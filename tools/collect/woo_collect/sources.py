from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
CLEAN = ROOT.parent.parent / "bronnen"

EXT = {"pdf": "pdf", "html": "html", "docx": "docx"}


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    section: str
    format: str
    url: str
    manual: bool = False

    @property
    def raw_path(self) -> Path:
        return RAW / f"{self.id}.{EXT[self.format]}"

    @property
    def meta_path(self) -> Path:
        return RAW / f"{self.id}.json"

    @property
    def clean_path(self) -> Path:
        return CLEAN / self.section / f"{self.id}.md"


def load_sources(path: Path = ROOT / "sources.yaml") -> list[Source]:
    return [Source(**entry) for entry in yaml.safe_load(path.read_text())]
