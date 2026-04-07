#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.hqi.ingest import ingest_books  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest local private books for the historical interview skill.")
    parser.add_argument("--config", required=True, help="Path to a private books JSON manifest.")
    parser.add_argument("--output", required=True, help="Writable output directory for processed artifacts.")
    args = parser.parse_args()

    summary = ingest_books(Path(args.config), Path(args.output))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
