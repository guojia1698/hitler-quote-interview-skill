# Private Corpus Setup

This public repository does not include any private books, local machine paths, or derived corpora.

To use a private corpus:

1. Copy [`private_books.template.json`](./private_books.template.json) to a local file outside the repository or to an ignored path such as `data/private_books/books.local.json`.
2. Replace each `source_path` with a real absolute path on your machine.
3. Run the ingestion script with an explicit config path.
4. Build the processed index into a local writable directory.

Example:

```bash
python3 skills/hitler-quote-interview/scripts/ingest_books.py \
  --config data/private_books/books.local.json \
  --output local-data/processed

python3 skills/hitler-quote-interview/scripts/build_index.py \
  --processed-dir local-data/processed
```

Then query the corpus:

```bash
python3 skills/hitler-quote-interview/scripts/query_corpus.py \
  --question "How do historians describe Hitler's rise to power?" \
  --processed-dir local-data/processed \
  --top-k 5
```
