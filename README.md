# LEGO Deal Finder — eBay + AI Prototype (No Discord)

This version is the local/testing stage of the LEGO Deal Finder. It searches eBay through the
official Browse API, optionally analyzes listing images with AI vision, calculates a simple
deal score, and prints qualifying listings to the terminal.

**Discord has intentionally been removed.** We can add the Discord bot later.

## What it does

1. Reads search settings from `.env`.
2. Gets an eBay Application Access Token.
3. Searches eBay's Browse API.
4. Calculates item + shipping total.
5. Optionally analyzes listing images with a vision-capable AI model.
6. Uses a configurable reference market price for the prototype deal calculation.
7. Prints qualifying deals and AI findings.
8. Stores processed eBay item IDs in SQLite.

## Important limitation

The market-price estimate is still a **prototype baseline**, not a real sold-comps valuation.
`REFERENCE_MARKET_PRICE_USD` is currently a single configurable reference value.

The next major development step should replace this with a LEGO-specific comparable-sales/market
pricing system.

## Windows setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with your eBay credentials. Add an OpenAI API key if you want image analysis.

Run:

```powershell
python main.py
```

Skip AI:

```powershell
python main.py --no-ai
```

## Example settings

```text
SEARCH_QUERY=LEGO 501st Clone Trooper
MAX_PRICE_USD=60
MIN_DISCOUNT_PERCENT=30
REFERENCE_MARKET_PRICE_USD=80
MAX_RESULTS=20
FIXED_PRICE_ONLY=true
```

## Later

Discord can be added as a separate layer after the eBay + AI + pricing pipeline is working.
The same scanning functions can then be called by a `/scan` command.
