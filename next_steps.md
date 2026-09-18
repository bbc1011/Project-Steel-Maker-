# Next upgrades

## 1. Real LEGO market valuation

Replace the single reference value with comparable-sales data and a LEGO-specific valuation
model that can account for condition, completeness, shipping, fees, and recency.

## 2. Better LEGO image identification

Add a LEGO catalog containing set numbers, minifigure IDs, visual descriptors, and historical
price ranges. Have the vision model return candidate IDs with confidence.

## 3. Multiple searches

Move from one `.env` search to a JSON/database configuration with separate rules per search.

## 4. Discord integration

Later add a full Discord bot with commands such as `/scan`, `/addsearch`, `/removesearch`,
`/searches`, and `/status`.

## 5. Server deployment

Once local testing is reliable, deploy the scanner to a suitable host. Since this version only
runs on command, there is no need for a continuous crawler yet.
