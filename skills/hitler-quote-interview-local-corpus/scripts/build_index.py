#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.hqi.index import build_index  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local retrieval index for the historical interview skill.")
    parser.add_argument("--processed-dir", required=True, help="Directory containing books_manifest.json and sections.jsonl.")
    parser.add_argument("--chunk-size", type=int, default=1200)
    args = parser.parse_args()

    summary = build_index(Path(args.processed_dir), chunk_size=args.chunk_size)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
