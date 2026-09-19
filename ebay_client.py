import base64
import time
from typing import Any, Dict, List

import requests

from models import Listing


class EbayClient:
    OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
    SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    def __init__(self, client_id: str, client_secret: str, marketplace_id: str,
                 timeout: int = 20, currency: str = "USD"):
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret are required")
        if not marketplace_id:
            raise ValueError("marketplace_id is required")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if not currency:
            raise ValueError("currency is required")

        self.client_id = client_id
        self.client_secret = client_secret
        self.marketplace_id = marketplace_id
        self.timeout = timeout
        self.currency = currency.upper()
        self._token: str | None = None
        self._expires_at = 0.0

    def _get_app_token(self) -> str:
        if self._token and time.time() < self._expires_at - 60:
            return self._token

        raw = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        encoded = base64.b64encode(raw).decode("ascii")

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        }

        response = requests.post(
            self.OAUTH_URL,
            headers=headers,
            data=data,
            timeout=self.timeout,
        )
        response.raise_for_status()

        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise RuntimeError("eBay OAuth response did not contain an access token")

        self._token = token
        self._expires_at = time.time() + int(payload.get("expires_in", 7200))
        return token

    def search(self, query: str, max_results: int = 20, max_price: float | None = None,
               fixed_price_only: bool = True) -> List[Listing]:
        query = query.strip()
        if not query:
            raise ValueError("query must not be empty")
        if max_results <= 0:
            raise ValueError("max_results must be greater than zero")
        if max_price is not None and max_price < 0:
            raise ValueError("max_price must not be negative")

        token = self._get_app_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
            "Accept": "application/json",
        }

        filters = []
        if max_price is not None:
            filters.append(f"price:[0..{max_price}],priceCurrency:{self.currency}")
        if fixed_price_only:
            filters.append("buyingOptions:{FIXED_PRICE}")

        params = {
            "q": query,
            "limit": min(max_results, 200),
        }
        if filters:
            params["filter"] = ",".join(filters)

        response = requests.get(
            self.SEARCH_URL,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload: Dict[str, Any] = response.json()

        listings: List[Listing] = []
        for item in payload.get("itemSummaries") or []:
            price = item.get("price") or {}
            shipping_cost = 0.0

            shipping = (item.get("shippingOptions") or [])
            if shipping:
                shipping_cost = float(
                    ((shipping[0].get("shippingCost") or {}).get("value")) or 0
                )

            image_url = None
            if item.get("image"):
                image_url = item["image"].get("imageUrl")

            additional_images = []
            for img in item.get("additionalImages") or []:
                if img.get("imageUrl"):
                    additional_images.append(img["imageUrl"])

            image_urls = [u for u in [image_url, *additional_images] if u]

            listings.append(
                Listing(
                    item_id=item.get("itemId", ""),
                    title=item.get("title", "Untitled"),
                    url=item.get("itemWebUrl", ""),
                    price=float(price.get("value") or 0),
                    currency=price.get("currency") or self.currency,
                    shipping=shipping_cost,
                    condition=item.get("condition"),
                    image_urls=image_urls,
                    seller_username=(item.get("seller") or {}).get("username"),
                    category_id=(item.get("categories") or [{}])[0].get("categoryId")
                    if item.get("categories") else None,
                )
            )

        return listings
