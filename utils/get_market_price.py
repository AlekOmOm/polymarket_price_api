import httpx
import asyncio

async def _midpoint(token_id: str, client: httpx.AsyncClient) -> float:
    bid_url = f"https://clob.polymarket.com/price?token_id={token_id}&side=buy"
    ask_url = f"https://clob.polymarket.com/price?token_id={token_id}&side=sell"
    bid_resp, ask_resp = await asyncio.gather(
        client.get(bid_url), client.get(ask_url)
    )
    bid_resp.raise_for_status()
    ask_resp.raise_for_status()
    bid = float(bid_resp.json()["price"])
    ask = float(ask_resp.json()["price"])
    return (bid + ask) / 2

async def get_market_price(token_id: str) -> float:
    """return midpoint price for the YES token"""
    async with httpx.AsyncClient(timeout=10) as client:
        return await _midpoint(token_id, client)
