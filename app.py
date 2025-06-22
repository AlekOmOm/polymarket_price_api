from fastapi import FastAPI, Query, HTTPException
from utils.common import slugify
from utils.check_market import check_market, cache_market
from utils.get_market_tokens import get_market_tokens
from utils.get_market_price import get_market_price

app = FastAPI(title="polymarket price api")

@app.get("/price")
async def price(market: str = Query(..., description="market slug or full url")):
    """
    Get midpoint price for a Polymarket YES token
    Returns: {"price": float} where float is between 0-1
    """
    slug = slugify(market)

    # 1. Token lookup: cache → gamma api
    tokens = check_market(slug)
    if not tokens:
        try:
            tokens = await get_market_tokens(slug)
            cache_market(slug, tokens)
        except Exception as exc:
            raise HTTPException(
                status_code=502, 
                detail=f"Failed to fetch market tokens: {str(exc)}"
            )

    # 2. Validate YES token exists
    yes_token = tokens.get("YES")
    if not yes_token:
        raise HTTPException(
            status_code=500, 
            detail=f"YES token not found. Available tokens: {list(tokens.keys())}"
        )

    # 3. Price fetch: bid/ask → midpoint
    try:
        price_value = await get_market_price(yes_token)
        return {"price": price_value}
    except Exception as exc:
        raise HTTPException(
            status_code=502, 
            detail=f"Price fetch failed: {str(exc)}"
        )

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
