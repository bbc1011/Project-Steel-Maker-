import json
from typing import List, Optional

from openai import OpenAI

from models import Listing, VisionResult


SYSTEM_PROMPT = """
You are a LEGO listing image analyst for a deal-finding application.

Analyze the provided e-commerce listing images conservatively.

Goals:
1. Identify LEGO sets, minifigures, recognizable characters, and notable components when
   reasonably visible.
2. Do not invent exact set numbers or minifigure IDs when the image is not clear enough.
3. Distinguish confidence from certainty.
4. Mention when an item may be obscured, duplicated, incomplete, or hard to identify.
5. Return strict JSON with keys:
   summary: short string
   items: array of strings
   confidence: number from 0 to 1
   caveats: array of strings

This is visual triage, not authentication or a guarantee of value.
""".strip()


def analyze_listing_images(api_key: str, model: str, listing: Listing,
                           max_images: int = 4) -> Optional[VisionResult]:
    if not api_key or not listing.image_urls:
        return None

    client = OpenAI(api_key=api_key)
    urls: List[str] = listing.image_urls[:max_images]

    content = [
        {
            "type": "input_text",
            "text": (
                f"Listing title: {listing.title}\n"
                f"Price: {listing.total_price:.2f} USD\n"
                "Identify what is visibly present in the photos. "
                "Do not rely solely on the title."
            ),
        }
    ]

    for url in urls:
        content.append(
            {
                "type": "input_image",
                "image_url": url,
            }
        )

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
    )

    text = response.output_text.strip()
    data = json.loads(text)

    confidence = float(data.get("confidence", 0))
    confidence = max(0.0, min(1.0, confidence))

    return VisionResult(
        summary=str(data.get("summary", "")),
        items=[str(x) for x in data.get("items", [])],
        confidence=confidence,
        caveats=[str(x) for x in data.get("caveats", [])],
    )
