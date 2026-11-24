"""Real local ONNX encoders on synthetic ranking tasks, with no answering LLM."""
from pathlib import Path
import argparse, csv, hashlib, json, math, platform, re, statistics, time
from collections import Counter
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer
ort.disable_telemetry_events()


def terms(text):return re.findall(r"[a-z0-9]+",text.lower())

def bm25(query, docs, k1=1.2, b=0.75):
    tokens=[terms(d["text"]) for d in docs];avg=sum(map(len,tokens))/len(tokens)
    dfs=Counter(t for ts in tokens for t in set(ts));q=terms(query);scores=[]
    for ts in tokens:
        tf=Counter(ts);score=0
        for t in q:
            df=dfs[t];idf=math.log(1+(len(tokens)-df+0.5)/(df+0.5))
            f=tf[t];score+=idf*f*(k1+1.0)/(f+k1*(1-b+b*len(ts)/avg))
        scores.append(score)
    return [int(i) for i in np.argsort(-np.array(scores),kind="stable")]


class Encoder:
    def __init__(self,path,max_length,threads=2):
        self.tokenizer=Tokenizer.from_file(str(path/"tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=max_length)
        self.tokenizer.enable_padding(pad_id=0,pad_token="[PAD]")
        opts=ort.SessionOptions();opts.intra_op_num_threads=threads;opts.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(path/"model.onnx"),sess_options=opts,providers=["CPUExecutionProvider"])
        self.input_names=[i.name for i in self.session.get_inputs()]
    def run(self,texts):
        enc=self.tokenizer.encode_batch(texts)
        values={"input_ids":np.array([e.ids for e in enc],dtype=np.int64),
                "attention_mask":np.array([e.attention_mask for e in enc],dtype=np.int64),
                "token_type_ids":np.array([e.type_ids for e in enc],dtype=np.int64)}
        outputs=self.session.run(None,{k:values[k] for k in self.input_names})
        return outputs,values["attention_mask"]
    def embed(self,texts):
        outputs,mask=self.run(texts);x=outputs[0]
        if x.ndim==3:x=(x*mask[:,:,None]).sum(axis=1)/np.maximum(mask.sum(axis=1)[:,None],1)
        return x/np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-12)
    def rerank(self,query,texts):
        outputs,_=self.run([(query,text) for text in texts]);return outputs[0].reshape(-1)


def metrics(order,docs,relevance):
    gains=[relevance.get(docs[i]["id"],0) for i in order]
    relevant=sum(1 for v in relevance.values() if v>0)
    rr=next((1/(i+1) for i,g in enumerate(gains[:10]) if g>0),0)
    recall=sum(g>0 for g in gains[:5])/relevant
    dcg=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(gains[:3]))
    ideal=sorted(relevance.values(),reverse=True)[:3]
    idcg=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(ideal))
    return {"mrr_at_10":rr,"recall_at_5":recall,"ndcg_at_3":dcg/idcg if idcg else 0}


def run(corpus_path,models,out):
    out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((models/"manifest.json").read_text())
    for model in manifest:
        for f in model["files"]:
            assert hashlib.sha256((models/model["id"]/f["local_file"]).read_bytes()).hexdigest()==f["sha256"],f
    corpus=json.loads(corpus_path.read_text());docs=corpus["documents"]
    start=time.perf_counter();embedding=Encoder(models/"embedding",256);reranker=Encoder(models/"reranker",512)
    load_ms=(time.perf_counter()-start)*1000
    embedding.embed(["Warm-up synthetic query"]);reranker.rerank("warm-up",["Synthetic evidence"])
    start=time.perf_counter();vectors=embedding.embed([d["text"] for d in docs]);build_ms=(time.perf_counter()-start)*1000
    rows=[];timings={"bm25":[],"dense":[],"hybrid_rrf":[],"hybrid_reranked":[]}
    for q in corpus["queries"]:
        t=time.perf_counter();sparse=bm25(q["text"],docs);sparse_ms=(time.perf_counter()-t)*1000
        t=time.perf_counter();v=embedding.embed([q["text"]])[0];dense=[int(i) for i in np.argsort(-(vectors@v),kind="stable")];dense_ms=(time.perf_counter()-t)*1000
        t=time.perf_counter();scores={}
        for ranking in (sparse[:5],dense[:5]):
            for rank,i in enumerate(ranking,1):scores[i]=scores.get(i,0)+1/(60+rank)
        hybrid=sorted(scores,key=lambda i:(-scores[i],i));merge_ms=(time.perf_counter()-t)*1000
        t=time.perf_counter();rs=reranker.rerank(q["text"],[docs[i]["text"] for i in hybrid]);reranked=[hybrid[int(i)] for i in np.argsort(-rs,kind="stable")];rerank_ms=(time.perf_counter()-t)*1000
        methods={"bm25":(sparse,sparse_ms),"dense":(dense,dense_ms),"hybrid_rrf":(hybrid,max(sparse_ms,dense_ms)+merge_ms),"hybrid_reranked":(reranked,max(sparse_ms,dense_ms)+merge_ms+rerank_ms)}
        for method,(order,elapsed) in methods.items():
            m=metrics(order,docs,q["relevance"]);timings[method].append(elapsed)
            rows.append({"query_id":q["id"],"method":method,**m,"estimated_path_ms":elapsed,"top_1":docs[order[0]]["id"],"candidate_count":len(order)})
    summary={}
    for method,values in timings.items():
        subset=[r for r in rows if r["method"]==method]
        summary[method]={k:statistics.mean(r[k] for r in subset) for k in ("mrr_at_10","recall_at_5","ndcg_at_3")}
        summary[method]["estimated_path_p50_ms"]=float(np.percentile(values,50));summary[method]["estimated_path_p95_ms"]=float(np.percentile(values,95))
    before=summary["hybrid_rrf"];after=summary["hybrid_reranked"]
    changes={k:after[k]-before[k] for k in ("mrr_at_10","recall_at_5","ndcg_at_3")}
    wins=ties=losses=0
    for q in corpus["queries"]:
        a=next(r for r in rows if r["query_id"]==q["id"] and r["method"]=="hybrid_rrf")
        c=next(r for r in rows if r["query_id"]==q["id"] and r["method"]=="hybrid_reranked")
        delta=c["ndcg_at_3"]-a["ndcg_at_3"]
        wins+=delta>1e-12;losses+=delta < -1e-12;ties+=abs(delta)<=1e-12
    result={"executed_at_utc":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "scope":corpus["scope"],"documents":len(docs),"queries":len(corpus["queries"]),"methods":summary,
            "reranker_delta_vs_hybrid":changes,"paired_ndcg_wins_ties_losses":{"wins":wins,"ties":ties,"losses":losses},
            "model_load_ms":load_ms,"document_embedding_ms":build_ms,"models":manifest,
            "runtime":{"python":platform.python_version(),"platform":platform.platform(),"onnxruntime":ort.__version__,"numpy":np.__version__,"threads":2},
            "timing_scope":"one sequential local run after one warm-up; hybrid path uses max(sparse,dense) estimate, not measured concurrent serving; not LLM TTFT or bank SLA",
            "limitations":["24 synthetic English texts", "18 author-defined queries and labels", "no independent adjudication or sealed holdout", "no answering LLM", "no Indian-language or scanned-image OCR evaluation", "no actual bank deployment"]}
    (out/"retrieval-results.json").write_text(json.dumps(result,indent=2)+"\n")
    with (out/"retrieval-per-query.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({"methods":summary,"reranker_delta":changes,"paired":result["paired_ndcg_wins_ties_losses"]},indent=2))
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--models",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    run(Path(__file__).resolve().parents[1]/"fixtures/retrieval-corpus.json",a.models,a.out)
