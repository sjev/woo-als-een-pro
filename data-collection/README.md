# Woo data collection

Step 1 of the knowledge base: fetch the sources in `sources.yaml` and convert them to clean markdown. This step is deterministic. It uses no LLM.

## Usage

```bash
uv sync
uv run python -m woo_collect all                  # fetch + extract
uv run python -m woo_collect fetch --refresh      # download again
uv run python -m woo_collect extract --only wet-woo
```

## Output

`data/raw/` and `data/last_run.json` are git-ignored. `data/clean/` is under version control, so changes to the cleaned text show in diffs.

| Path | Content |
|---|---|
| `data/raw/<id>.<ext>` | original file |
| `data/raw/<id>.json` | url, fetched_at, sha256 |
| `data/clean/<section>/<id>.md` | markdown with YAML front matter |
| `data/last_run.json` | status per source |

## Sources

- `sources.yaml` is the machine-readable list. `sources.md` holds the human notes.
- Laws come from the BWB XML repository (the version in force today), resolved through the SRU service of zoekservice.overheid.nl. Use `chapters` to limit a large law.
- `manual: true` means the site blocks automated downloads. Download the file in a browser and save it as `data/raw/<id>.pdf`. Then run `extract`.
