from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Listing:
    item_id: str
    title: str
    url: str
    price: float
    currency: str
    shipping: float = 0.0
    condition: Optional[str] = None
    image_urls: Optional[List[str]] = None
    seller_username: Optional[str] = None
    category_id: Optional[str] = None

    @property
    def total_price(self) -> float:
        return round(self.price + self.shipping, 2)


@dataclass
class VisionResult:
    summary: str
    items: List[str]
    confidence: float
    caveats: List[str]


@dataclass
class Deal:
    listing: Listing
    market_price: float
    discount_percent: float
    score: float
    ai: Optional[VisionResult] = None
