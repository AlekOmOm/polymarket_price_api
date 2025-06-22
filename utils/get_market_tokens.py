import httpx
import asyncio
from .common import slugify

async def get_market_tokens(slug: str) -> dict:
    """
    Fetch market tokens from gamma API and return {YES: id, NO: id} dict
    """
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        
        if not data:
            raise ValueError(f"No market found for slug '{slug}'")
            
        market = data[0] if isinstance(data, list) else data
        
        # Build token mapping
        tokens = {}
        for token in market["tokens"]:
            name = token["name"].upper()  # YES/NO
            tokens[name] = token["id"]
            
        return tokens

# Keep CLI functionality for testing
def fetch_tokens(slug: str):
    """Sync version for CLI usage"""
    import requests
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise SystemExit(f"no market found for slug '{slug}'")
    market = data[0] if isinstance(data, list) else data
    return [(t["name"], t["symbol"], t["id"]) for t in market["tokens"]]

def main():
    import sys
    if len(sys.argv) != 2:
        print("usage: python get_market_tokens.py <market-slug-or-url>")
        sys.exit(1)
    slug = slugify(sys.argv[1])
    for name, sym, tid in fetch_tokens(slug):
        print(f"{name:>3} ({sym}) → {tid}")

if __name__ == "__main__":
    main()
