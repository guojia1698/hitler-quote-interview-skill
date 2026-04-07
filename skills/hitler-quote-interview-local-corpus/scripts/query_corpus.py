#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.hqi.query import query_corpus  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the local historical interview corpus.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--processed-dir", required=True, help="Directory containing chunks.jsonl.")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    result = query_corpus(args.question, Path(args.processed_dir), top_k=args.top_k)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
