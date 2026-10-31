# collect

Fetch the sources in `sources.yaml` and convert them to clean markdown in [`../../bronnen/`](../../bronnen/README.md). The step is deterministic. It uses no LLM. Law text is out of scope: use [`../wetten.py`](../README.md#wettenpy).

## Usage

Run from this folder:

```bash
uv sync
uv run python -m woo_collect all                  # fetch + extract
uv run python -m woo_collect fetch --refresh      # download again
uv run python -m woo_collect extract --only woo-witboek
```

## Output

| Path | Content | In git |
|---|---|---|
| `data/raw/<id>.<ext>` | original file | no |
| `data/raw/<id>.json` | url, fetched_at, sha256 | no |
| `data/last_run.json` | status per source | no |
| `../../bronnen/<section>/<id>.md` | markdown with YAML front matter | yes, so changes show in diffs |

## Sources

- `sources.yaml` is the machine-readable list. Human notes per source are in [`../../bronnen/README.md`](../../bronnen/README.md).
- `manual: true` means the site blocks automated downloads. Download the file in a browser and save it as `data/raw/<id>.<ext>`. Then run `extract`.
