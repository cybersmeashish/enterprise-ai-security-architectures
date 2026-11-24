"""Execute bounded tests and planning; optionally run the cached real retrieval models."""
from pathlib import Path
import argparse,datetime,hashlib,io,json,os,platform,re,socket,subprocess,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from core import capacity,generation_cost,clause_chunks,CacheScope,ScopedSemanticCache,route_model,bounded_tool_plan,safe_envelope
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]


def local_links():
    count=0
    paths=list(ROOT.rglob("*.md"))+[REPO/"README.md",REPO/"AGENTS.md",REPO/"products/README.md"]
    for path in paths:
        if "evidence" in path.relative_to(REPO).parts:continue
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)",path.read_text()):
            if target.startswith(("https://","http://","#","mailto:")):continue
            target=target.split("#")[0]
            if not (path.parent/target).resolve().exists():raise AssertionError(f"Broken document link: {path}: {target}")
            count+=1
    return count


def isolation():
    interfaces=sorted(Path("/sys/class/net").iterdir());names=[p.name for p in interfaces]
    with socket.socket() as s:
        s.settimeout(1)
        try:s.connect(("198.51.100.1",443));out={"probe":"unexpected_connection"}
        except OSError as e:out={"probe":"blocked","errno":e.errno,"exception":type(e).__name__}
    routes=Path("/proc/net/route").read_text().splitlines()[1:]
    default=any(line.split()[1]=="00000000" for line in routes if len(line.split())>1)
    out.update({"interfaces":names,"default_ipv4_route":default,"uid":os.getuid(),"root_read_only":bool(os.statvfs("/").f_flag & os.ST_RDONLY),"workspace_read_only":bool(os.statvfs(str(ROOT)).f_flag & os.ST_RDONLY)})
    if names!=["lo"] or default or out.get("errno")!=101:raise AssertionError("External-network isolation not established")
    return out


def verify(output,models=None,isolated=False):
    output.mkdir(parents=True,exist_ok=True)
    suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"));count=suite.countTestCases();log=io.StringIO()
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    (output/"tests.log").write_text(log.getvalue())
    if not result.wasSuccessful():raise AssertionError(log.getvalue())
    # Validate the authored specification, never imply support answers were generated.
    spec=json.loads((ROOT/"fixtures/support-eval-spec.json").read_text());cases=spec["cases"]
    assert len(cases)==len({c["id"] for c in cases})==30
    decisions=json.loads((ROOT/"fixtures/decision-register.json").read_text())
    assert len(decisions)==len({c["id"] for c in decisions})==18
    assert all((ROOT/c["path"]).is_file() for c in decisions)
    corpus=json.loads((ROOT/"fixtures/retrieval-corpus.json").read_text())
    docids={d["id"] for d in corpus["documents"]}
    assert len(docids)==24 and len(corpus["queries"])==18
    assert all(set(q["relevance"])<=docids for q in corpus["queries"])
    sources=json.loads((ROOT/"fixtures/source-register.json").read_text())
    cp=json.loads((ROOT/"fixtures/capacity.json").read_text());cost=json.loads((ROOT/"fixtures/cost-scenario.json").read_text())
    scenarios={"capacity":capacity(cp),"cost":generation_cost(cost),"page_sensitivity":{str(n):capacity(dict(cp,pages_per_document=n)) for n in (1,6,20)}}
    (output/"planning-results.json").write_text(json.dumps(scenarios,indent=2)+"\n")
    scope=CacheScope("SYN","employee-A","case-A","support",3,"c1","p1","en","2026-11-24")
    cache=ScopedSemanticCache();cache.put(scope,"generic_notice",["45"],"SYN answer",100)
    hit=cache.get(scope,"generic_notice",["45"],0.99,50,True,True)
    revoked=cache.get(scope,"generic_notice",["45"],0.99,50,True,False)
    cache.get(scope,"generic_notice",["45"],0.99,50,False,True)
    calls=[{"tool":"lookup","args":{"id":"SYN1"},"state_version":1}]*2
    observations={"valid_cache_hit":hit is not None,"revoked_grant_cache_blocked":revoked is None,"cache_metrics":cache.metrics(),
                  "loop":bounded_tool_plan(calls,{"lookup"}),"invalid_json_output":json.loads(safe_envelope("invalid",set())),
                  "chunk_count":len(clause_chunks(json.loads((ROOT/"fixtures/legal-contract.json").read_text()))),
                  "scope":"synthetic boundary examples, not identity integration or bank tools"}
    (output/"lab-observations.json").write_text(json.dumps(observations,indent=2)+"\n")
    if models:
        from retrieval_benchmark import run
        run(ROOT/"fixtures/retrieval-corpus.json",models,output)
    checked=local_links()
    # Newly authored source plus the three edited portfolio paths and repository instructions.
    paths=[p for p in ROOT.rglob("*") if p.is_file() and "evidence" not in p.relative_to(ROOT).parts and "__pycache__" not in p.parts and p.suffix!=".pyc"]
    paths += [REPO/"README.md",REPO/"products/README.md",REPO/"docs/index.html",REPO/"AGENTS.md"]
    manifest={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
    (output/"source-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    def cgroup(name):
        p=Path("/sys/fs/cgroup")/name
        return p.read_text().strip() if p.is_file() else "unavailable"
    record={"executed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"runtime":{"python":platform.python_version(),"system":platform.system(),"machine":platform.machine(),"cpu_quota":cgroup("cpu.max"),"memory_limit_bytes":cgroup("memory.max")},
            "unique_regression_tests":count,"support_eval_specification_cases":len(cases),"support_llm_outcomes_executed":False,
            "architecture_decisions":len(decisions),"requested_capability_groups":25,"local_links_checked":checked,"source_manifest_files":len(manifest),
            "primary_references_content_reviewed":sum(x["content_review_status"]=="retrieved_reference" for x in sources),
            "learned_retrieval_executed":bool(models),"retrieval_documents":len(corpus["documents"]),"retrieval_queries":len(corpus["queries"]),
            "network_isolation":isolation() if isolated else {"requested":False},
            "scope":"planning/guardrail tests and optional actual synthetic learned-model ranking; no production bank ingestion, support LLM quality, 70% savings or TTFT claim"}
    (output/"verification.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record,indent=2));return record

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--models",type=Path);p.add_argument("--isolated",action="store_true");a=p.parse_args();verify(a.output,a.models,a.isolated)
