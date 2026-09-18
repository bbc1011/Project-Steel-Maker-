import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


def require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def as_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name, str(default)).strip().lower()
    return raw in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Config:
    ebay_client_id: str
    ebay_client_secret: str
    ebay_marketplace_id: str
    search_query: str
    max_price_usd: float
    min_discount_percent: float
    max_results: int
    fixed_price_only: bool
    reference_market_price_usd: float
    openai_api_key: str
    openai_model: str
    ai_max_images: int
    database_path: str
    request_timeout_seconds: int


def load_config() -> Config:
    return Config(
        ebay_client_id=require("EBAY_CLIENT_ID"),
        ebay_client_secret=require("EBAY_CLIENT_SECRET"),
        ebay_marketplace_id=os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US").strip(),
        search_query=require("SEARCH_QUERY"),
        max_price_usd=float(os.getenv("MAX_PRICE_USD", "60")),
        min_discount_percent=float(os.getenv("MIN_DISCOUNT_PERCENT", "30")),
        max_results=int(os.getenv("MAX_RESULTS", "20")),
        fixed_price_only=as_bool("FIXED_PRICE_ONLY", True),
        reference_market_price_usd=float(
            os.getenv("REFERENCE_MARKET_PRICE_USD", "80")
        ),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna").strip(),
        ai_max_images=max(1, int(os.getenv("AI_MAX_IMAGES", "4"))),
        database_path=os.getenv("DATABASE_PATH", "deal_finder.db").strip(),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")),
    )
