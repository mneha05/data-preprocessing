from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from urllib import request


def put_row(rest: str, table: str, row_key: str, record: dict) -> None:
    cells = []
    for key, value in record.items():
        cells.append({
            "column": base64.b64encode(f"d:{key}".encode()).decode(),
            "$": base64.b64encode(str(value).encode()).decode(),
        })
    payload = json.dumps({
        "Row": [{"key": base64.b64encode(row_key.encode()).decode(), "Cell": cells}]
    }).encode()

    req = request.Request(
        f"{rest.rstrip('/')}/{table}/{row_key}",
        data=payload,
        method="PUT",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with request.urlopen(req, timeout=10):
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--rest", default="http://localhost:8080")
    p.add_argument("--table", default="gpu_telemetry")
    args = p.parse_args()

    with args.input.open() as f:
        for i, line in enumerate(f):
            put_row(args.rest, args.table, str(i), json.loads(line))


if __name__ == "__main__":
    main()
