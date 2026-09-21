from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib import request

try:
    import cudf
    BACKEND = "cudf"
except Exception:
    cudf = None
    import pandas as pd
    BACKEND = "pandas"


def load_frame(path: Path):
    if BACKEND == "cudf":
        return cudf.read_json(path, lines=True)
    return pd.read_json(path, lines=True)


def summarize(df):
    grouped = (
        df.groupby(["service", "gpu_id"])
        .agg({"latency_ms": ["mean", "max"], "errors": "sum", "requests": "sum"})
        .reset_index()
    )
    if BACKEND == "cudf":
        grouped = grouped.to_pandas()
    grouped.columns = [
        "_".join(str(x) for x in col if x).rstrip("_") if isinstance(col, tuple) else str(col)
        for col in grouped.columns
    ]
    return grouped


def bulk_index(path: Path, endpoint: str, index: str) -> None:
    body = bytearray()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            payload = json.loads(line)
            body += (json.dumps({"index": {"_index": index}}) + "\n").encode()
            body += (json.dumps(payload) + "\n").encode()

    req = request.Request(
        endpoint.rstrip("/") + "/_bulk",
        data=bytes(body),
        method="POST",
        headers={"Content-Type": "application/x-ndjson"},
    )
    with request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    if result.get("errors"):
        raise RuntimeError("Elasticsearch bulk indexing reported errors")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--summary", type=Path, default=Path("summary.json"))
    p.add_argument("--elasticsearch")
    p.add_argument("--index", default="gpu-telemetry")
    args = p.parse_args()

    df = load_frame(args.input)
    summary = summarize(df)
    args.summary.write_text(summary.to_json(orient="records", indent=2) + "\n")

    print(f"backend={BACKEND} rows={len(df)} summary={args.summary}")
    if args.elasticsearch:
        bulk_index(args.input, args.elasticsearch, args.index)
        print(f"indexed into {args.elasticsearch}/{args.index}")


if __name__ == "__main__":
    main()
