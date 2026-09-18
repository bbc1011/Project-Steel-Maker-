from models import Deal, Listing, VisionResult


def calculate_discount_percent(market_price: float, total_price: float) -> float:
    if market_price <= 0:
        return 0.0
    return round((market_price - total_price) / market_price * 100, 1)


def calculate_deal_score(discount_percent: float, ai_confidence: float = 0.0) -> float:
    # Simple prototype score. Later we can incorporate condition, seller quality,
    # completeness, recent sold comps, demand, and category-specific signals.
    discount_component = max(0.0, min(discount_percent / 50.0, 1.0))
    ai_component = max(0.0, min(ai_confidence, 1.0))
    score = 10.0 * (0.8 * discount_component + 0.2 * ai_component)
    return round(score, 1)


def evaluate(listing: Listing, market_price: float,
             min_discount_percent: float,
             ai: VisionResult | None = None) -> Deal | None:
    discount = calculate_discount_percent(market_price, listing.total_price)
    if discount < min_discount_percent:
        return None

    ai_conf = ai.confidence if ai else 0.0
    score = calculate_deal_score(discount, ai_conf)

    return Deal(
        listing=listing,
        market_price=market_price,
        discount_percent=discount,
        score=score,
        ai=ai,
    )
