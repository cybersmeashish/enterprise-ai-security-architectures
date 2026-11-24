"""Synthetic planning and boundary examples; no production banking or LLM adapter."""
from __future__ import annotations
import hashlib, json, math, re
from dataclasses import dataclass
from typing import Any


def positive(value: Any, name: str, zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    if value < 0 or (value == 0 and not zero):
        raise ValueError(name + " is outside its range")
    return float(value)


def capacity(cfg: dict) -> dict:
    v={k:positive(cfg[k], k) for k in (
        "documents", "month_days", "pages_per_document", "tokens_per_page",
        "chunks_per_document", "retry_amplification", "ocr_seconds_per_page",
        "worker_utilisation", "burst_multiplier", "capture_days", "capture_hours_per_day",
        "scanner_pages_per_minute", "scanner_utilisation", "image_bytes_per_page",
        "vector_dimensions", "vector_bytes_per_value", "vector_index_factor", "copies")}
    if any(not v[k].is_integer() for k in ("documents", "copies", "vector_dimensions", "vector_bytes_per_value")):
        raise ValueError("document counts, replicas and vector dimensions/bytes must be whole numbers")
    if v["worker_utilisation"] > 1 or v["scanner_utilisation"] > 1 or v["capture_hours_per_day"] > 24:
        raise ValueError("invalid utilisation or daily hours")
    if v["capture_days"] > v["month_days"] or v["retry_amplification"] < 1 or v["burst_multiplier"] < 1 or v["copies"] < 1 or v["vector_index_factor"] < 1:
        raise ValueError("invalid month/amplification/copies")
    seconds=v["month_days"]*86400
    pages=v["documents"]*v["pages_per_document"]
    pps=pages/seconds
    processed_pps=pps*v["retry_amplification"]
    capture_minutes=v["capture_days"]*v["capture_hours_per_day"]*60
    vectors=v["documents"]*v["chunks_per_document"]*v["vector_dimensions"]*v["vector_bytes_per_value"]
    return {
        "scope":"calculated assumptions, not measured throughput",
        "documents_per_second":v["documents"]/seconds,
        "pages_per_month":pages,
        "pages_per_second":pps,
        "processed_pages_per_second":processed_pps,
        "ocr_workers_average":math.ceil(processed_pps*v["ocr_seconds_per_page"]/v["worker_utilisation"]),
        "ocr_workers_burst":math.ceil(processed_pps*v["burst_multiplier"]*v["ocr_seconds_per_page"]/v["worker_utilisation"]),
        "scanner_stations_assumed_schedule":math.ceil(pages/(capture_minutes*v["scanner_pages_per_minute"]*v["scanner_utilisation"])),
        "embedding_tokens_per_month":pages*v["tokens_per_page"]*v["retry_amplification"],
        "embedding_tokens_per_second":pages*v["tokens_per_page"]*v["retry_amplification"]/seconds,
        "chunks_per_month":v["documents"]*v["chunks_per_document"],
        "original_images_TB_one_copy":pages*v["image_bytes_per_page"]/1e12,
        "original_images_TB_all_copies":pages*v["image_bytes_per_page"]*v["copies"]/1e12,
        "vectors_TB_values_only":vectors/1e12,
        "vectors_TB_with_factor_and_copies":vectors*v["vector_index_factor"]*v["copies"]/1e12,
        "excluded":["conservation", "handling and QA", "text/sparse index", "metadata", "retained generations", "LLM serving", "staff coverage", "actual performance"]}


def generation_cost(cfg: dict) -> dict:
    n=positive(cfg["requests"], "requests")
    hit=positive(cfg["cache_hit_fraction"],"cache_hit_fraction",True)
    cheap=positive(cfg["cheap_fraction_of_misses"],"cheap_fraction_of_misses",True)
    if hit>1 or cheap>1:raise ValueError("fractions exceed one")
    def spend(tokens, rates):
        return sum(positive(tokens[k],k,True)*positive(rates[k],k,True)/1e6 for k in ("input","output"))
    baseline=n*spend(cfg["baseline_tokens"],cfg["smart_rates"])
    misses=n*(1-hit)
    proposed=misses*(cheap*spend(cfg["proposed_tokens"],cfg["cheap_rates"])+(1-cheap)*spend(cfg["proposed_tokens"],cfg["smart_rates"]))
    return {"baseline_generation_cost":baseline,"proposed_generation_cost":proposed,
            "generation_saving_fraction":None if baseline==0 else 1-proposed/baseline,
            "rates":"hypothetical fixture currency units per million tokens; not commercial quotes",
            "quality_verified":False,"excluded_costs":["OCR","embedding","retrieval/rerank","GPU idle capacity","cache","human review","network"]}


def clause_chunks(doc: dict, max_words=120, overlap_words=15) -> list[dict]:
    """Uses whitespace words, not model tokens; retains structured clause provenance."""
    if isinstance(max_words,bool) or not isinstance(max_words,int) or max_words<2 or isinstance(overlap_words,bool) or not isinstance(overlap_words,int) or not 0<=overlap_words<max_words:
        raise ValueError("invalid chunk bounds")
    out=[]
    for clause in doc["clauses"]:
        words=clause["text"].split();start=0;part=0
        while start<len(words):
            end=min(len(words),start+max_words)
            out.append({"doc_id":doc["doc_id"],"version":doc["version"],"clause":clause["path"],
                        "parent_id":clause["parent_id"],"pages":clause["pages"],"references":clause.get("references",[]),
                        "scope":doc["scope"],"part":part,"word_start":start,"word_end":end,"text":" ".join(words[start:end])})
            if end==len(words):break
            start=end-overlap_words;part+=1
    return out


def authorised(record: dict, grant: dict) -> bool:
    """Synthetic, already-verified server grant; no authentication implementation."""
    required=("bank","case","purpose")
    if any(not isinstance(record.get(k),str) or not record[k] or not isinstance(grant.get(k),str) or not grant[k] for k in required):return False
    if type(record.get("epoch")) is not int or type(grant.get("epoch")) is not int or record["epoch"]<0 or grant["epoch"]<0:return False
    return (grant.get("verified") is True and record.get("bank")==grant.get("bank")
            and record.get("case")==grant.get("case") and record.get("purpose")==grant.get("purpose")
            and record.get("epoch")==grant.get("epoch") and record.get("revoked") is not True)


PII_RULES=[("EMAIL",re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
           ("PAN",re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")),
           ("AADHAAR_LIKE",re.compile(r"\b[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}\b"))]
def redact_synthetic(text: str) -> dict:
    """Limited patterns only; no guarantee of finding all PII or validating Aadhaar."""
    counts={}
    for label,rule in PII_RULES:
        text,n=rule.subn("["+label+"]",text)
        if n:counts[label]=n
    return {"text":text,"matches":counts,"complete_pii_detection":False}


@dataclass(frozen=True)
class CacheScope:
    bank: str
    subject_group: str
    case: str
    purpose: str
    permission_epoch: int
    corpus_version: str
    release: str
    language: str
    as_of: str


class ScopedSemanticCache:
    """Scores supplied by an approved encoder; same-scope checks independently enforced."""
    def __init__(self, threshold=0.97):
        if not 0<threshold<=1:raise ValueError("invalid cosine threshold")
        self.threshold=threshold;self.entries=[]
        self.stats={"total":0,"eligible":0,"probes":0,"hits":0,"expired":0,"rejected":0}
    def put(self, scope, intent, important_values, answer, expires):
        self.entries.append((scope,intent,tuple(important_values),answer,positive(expires,"expires")))
    def get(self, scope, intent, important_values, similarity, now, eligible, grants_current):
        if type(eligible) is not bool or type(grants_current) is not bool:raise ValueError("cache flags must be verified booleans")
        self.stats["total"]+=1
        if not eligible:return None
        self.stats["eligible"]+=1
        if not grants_current:return None
        self.stats["probes"]+=1
        positive(now,"now",True)
        if isinstance(similarity,bool) or not isinstance(similarity,(int,float)) or not math.isfinite(similarity) or not -1<=similarity<=1:
            raise ValueError("invalid similarity")
        for s,i,values,answer,expires in self.entries:
            if s!=scope:continue
            if expires<=now:self.stats["expired"]+=1;continue
            if i!=intent or values!=tuple(important_values) or similarity<self.threshold:
                self.stats["rejected"]+=1;continue
            self.stats["hits"]+=1;return answer
        return None
    def metrics(self):
        s=dict(self.stats)
        s["hit_rate_total"]=s["hits"]/s["total"] if s["total"] else 0
        s["hit_rate_eligible"]=s["hits"]/s["eligible"] if s["eligible"] else 0
        return s


def route_model(*, permitted: bool, supported_language: bool, evidence_sufficient: bool, material: bool, conflict: bool, ocr_uncertain: bool) -> str:
    flags=(permitted,supported_language,evidence_sufficient,material,conflict,ocr_uncertain)
    if any(type(x) is not bool for x in flags):raise ValueError("trusted routing flags must be booleans")
    if not permitted:return "deny"
    if not supported_language or not evidence_sufficient:return "human_review"
    if material or conflict or ocr_uncertain:return "smart_or_human_review"
    return "cheap"


def bounded_tool_plan(calls: list[dict], allowed: set[str], max_steps=8) -> dict:
    """Plan inspection only; never executes a bank tool or action."""
    if isinstance(max_steps,bool) or not isinstance(max_steps,int) or max_steps<1:raise ValueError("invalid step budget")
    seen=set();steps=[]
    for call in calls:
        if len(steps)>=max_steps:return {"status":"needs_review","reason":"step_budget","steps":steps}
        if call.get("tool") not in allowed:return {"status":"denied","reason":"unregistered_tool","steps":steps}
        raw=json.dumps([call["tool"],call.get("args",{}),call.get("state_version")],sort_keys=True,separators=(",",":"),allow_nan=False)
        key=hashlib.sha256(raw.encode()).hexdigest()
        if key in seen:return {"status":"needs_review","reason":"no_progress_loop","steps":steps}
        seen.add(key);steps.append({"tool":call["tool"],"call_hash":key})
    return {"status":"plan_bounded","steps":steps,"execution":False}


def parse_answer(raw: str, allowed_citations: set[str]) -> dict:
    """Bounded schema demonstration; validity is not truth or production authority."""
    if not isinstance(raw,str):raise ValueError("answer must be text")
    if len(raw.encode())>32768:raise ValueError("answer too large")
    def pairs(xs):
        out={}
        for k,v in xs:
            if k in out:raise ValueError("duplicate key")
            out[k]=v
        return out
    def bad_number(x):raise ValueError("non-finite JSON")
    try:a=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad_number)
    except (RecursionError,json.JSONDecodeError) as e:raise ValueError("invalid JSON") from e
    if not isinstance(a,dict) or set(a)!={"status","answer","citations","uncertainty"}:raise ValueError("unknown/missing fields")
    if a["status"] not in ("answered","needs_review","denied","error") or not isinstance(a["answer"],str) or not isinstance(a["uncertainty"],str):raise ValueError("invalid fields")
    if not isinstance(a["citations"],list) or len(a["citations"])>20 or any(not isinstance(x,str) or x not in allowed_citations for x in a["citations"]):raise ValueError("invalid citation")
    if a["status"]=="answered" and (not a["answer"].strip() or not a["citations"]):raise ValueError("answered requires evidence")
    if a["status"] in ("denied","error") and a["citations"]:raise ValueError("denial/error must not disclose sources")
    return a


def safe_envelope(raw: str, allowed_citations: set[str]) -> str:
    try:a=parse_answer(raw,allowed_citations)
    except (ValueError,TypeError):a={"status":"error","answer":"","citations":[],"uncertainty":"Invalid or unsupported response; human review required."}
    return json.dumps(a,allow_nan=False,separators=(",",":"))
