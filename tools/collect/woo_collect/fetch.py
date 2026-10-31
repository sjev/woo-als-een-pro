import hashlib
import json
import time
from datetime import datetime, timezone

import httpx

from woo_collect.sources import RAW, Source

USER_AGENT = "woo-als-een-pro-collector/0.1 (research; low volume)"
DELAY_S = 1.0

# A server that returns an HTML error or challenge page instead of the file must not count as success.
EXPECTED_TYPES = {
    "pdf": ("application/pdf",),
    "docx": ("application/vnd.openxmlformats", "application/octet-stream"),
    "html": ("text/html",),
}


def client() -> httpx.Client:
    return httpx.Client(headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=60)


def fetch(source: Source, http: httpx.Client, refresh: bool = False) -> str:
    if source.raw_path.exists() and not refresh:
        return "cached"
    if source.manual:
        return f"manual: download {source.url} to {source.raw_path}"

    url = source.url
    time.sleep(DELAY_S)
    resp = http.get(url)
    content_type = resp.headers.get("content-type", "")
    if resp.status_code != 200:
        return f"error: HTTP {resp.status_code}"
    if not content_type.startswith(EXPECTED_TYPES[source.format]):
        return f"error: unexpected content-type {content_type!r}"

    RAW.mkdir(parents=True, exist_ok=True)
    source.raw_path.write_bytes(resp.content)
    meta = {
        "url": url,
        "final_url": str(resp.url),
        "content_type": content_type,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(resp.content).hexdigest(),
    }
    source.meta_path.write_text(json.dumps(meta, indent=2))
    return f"ok ({len(resp.content) // 1024} KiB)"
