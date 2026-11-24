"""Download only the exact public artifacts recorded for the synthetic experiment."""
from pathlib import Path
import argparse,hashlib,json,urllib.request

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--destination",type=Path,required=True);a=p.parse_args()
    manifest=json.loads((Path(__file__).resolve().parents[1]/"evidence/model-manifest.json").read_text())
    for model in manifest:
        if model["repository"] not in ("sentence-transformers/all-MiniLM-L6-v2","cross-encoder/ms-marco-MiniLM-L6-v2"):
            raise RuntimeError("unapproved model repository")
        folder=a.destination/model["id"];folder.mkdir(parents=True,exist_ok=True)
        for item in model["files"]:
            path=folder/item["local_file"]
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==item["sha256"]:continue
            url="https://huggingface.co/"+model["repository"]+"/resolve/"+model["revision"]+"/"+item["source_file"]
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Banking-RAG-reference/0.1"}),timeout=120) as r:
                raw=r.read(item["bytes"]+1)
            if len(raw)!=item["bytes"] or hashlib.sha256(raw).hexdigest()!=item["sha256"]:raise RuntimeError("artifact mismatch: "+url)
            path.write_bytes(raw)
    (a.destination/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Exact model artifacts verified; weights remain outside public source.")
