# Polymarket Price API

get price (probability) of a event

- request: with market url
- response: price  

## dir
```plaintext

polymarket_price_api/
├── app.py                  # fastapi entry
├── requirements.txt
├── db/
│   └── markets.json        # simple token-cache (starts empty)
├── utils/
│   ├── __init__.py
│   ├── common.py           # slugify helper
│   ├── check_market.py     # cache lookup / write-back
│   ├── get_market_tokens.py# gamma api → tokens
│   └── get_market_price.py # clob api → midpoint
└── tests/
    └── test_price.py       # sanity integration test
```


## main flow 

### get price for a market



```bash

user ──> fastapi /price?market=<slug|url>
          |
          v
      get_market_token_data()
          |
          |-- check_market(slug) ──> db/markets.json
          |         |                (cached tokens?)
          |         └─╴ if hit -> tokens
          |
          |-- get_market_tokens(slug)        # external call
          |         └─ store in db           # write-back cache
          v
      tokens = {"YES": id_yes, "NO": id_no}

      get_market_price(tokens)
          |
          |-- call /price?id_yes&side=buy
          |-- call /price?id_yes&side=sell
          |   ... same for id_no if needed
          |
          |-- avg = (bid + ask) / 2
          v
      return {"price": avg}
```
## 
**tldr**

* single-endpoint microservice (`/price?market=<slug|url>`) exposing the midpoint ( best-bid + best-ask )/2 for a Polymarket *YES* token
* built on **fastapi** + **httpx** (async)
* request flow

  1. **slugify** input (url or slug) → canonical slug
  2. **check\_market** → local `db/markets.json` cache for `{YES, NO}` token-ids
  3. cache miss → **get\_market\_tokens** hits *gamma* API, stores tokens back to cache
  4. **get\_market\_price** hits *clob* `/price` for bid & ask → returns midpoint
* returns `{ "price": <float 0–1> }` or 5xx on upstream failure
* thin file-based cache (easy to swap for redis/sqlite)
* lightweight test in `tests/` does gamma+clob round-trip sanity check
* install -> `pip install -r requirements.txt`; run -> `uvicorn app:app --reload`

