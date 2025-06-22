from pathlib import Path
import json
from .common import slugify

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "markets.json"

def _load_db() -> dict:
    if DB_PATH.exists():
        with DB_PATH.open() as f:
            return json.load(f)
    return {}

def check_market(slug_or_url: str):
    """return cached token dict or None"""
    slug = slugify(slug_or_url)
    return _load_db().get(slug)

def cache_market(slug: str, tokens: dict):
    """write-back cache after fresh fetch"""
    data = _load_db()
    data[slug] = tokens
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w") as f:
        json.dump(data, f, indent=2)
