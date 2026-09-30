"""
Part One: Camera sale.

Reads the raw product data, reduces the price of every product in the
"Cameras & Camcorders" category by 20% (rounded down to the nearest whole
number), and uploads the full catalogue to Algolia in a single run.

Usage:
    python scripts/upload_products.py            # transform + upload
    python scripts/upload_products.py --dry-run  # transform only, print a summary
"""

import argparse
import json
import math
import os
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"

SALE_CATEGORY = "Cameras & Camcorders"
DISCOUNT = Decimal("0.20")

# Price buckets used by the source data's `price_range` attribute (upper bound inclusive).
PRICE_RANGES = [(50, "1 - 50"), (100, "50 - 100"), (200, "100 - 200"), (500, "200 - 500"), (2000, "500 - 2000")]


def is_on_sale(product: dict) -> bool:
    return product["hierarchicalCategories"].get("lvl0") == SALE_CATEGORY


def discounted_price(price: float) -> int:
    # Decimal avoids float artefacts (e.g. 79.99999 flooring to 79 instead of 80).
    return math.floor(Decimal(str(price)) * (1 - DISCOUNT))


def price_range_for(price: float) -> str:
    for upper, label in PRICE_RANGES:
        if price <= upper:
            return label
    return "> 2000"


def transform(products: list[dict]) -> list[dict]:
    for product in products:
        if is_on_sale(product):
            product["price"] = discounted_price(product["price"])
            # Keep the price_range facet consistent with the new price.
            product["price_range"] = price_range_for(product["price"])
    return products


def upload(products: list[dict]) -> None:
    from algoliasearch.search.client import SearchClientSync

    load_dotenv()
    app_id = os.environ["ALGOLIA_APP_ID"]
    api_key = os.environ["ALGOLIA_ADMIN_API_KEY"]  # write access needed; never ship this to the front end
    index_name = os.environ["ALGOLIA_INDEX"]

    client = SearchClientSync(app_id, api_key)
    client.save_objects(index_name, products, wait_for_tasks=True)
    print(f"Uploaded {len(products)} records to '{index_name}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="transform only, do not upload")
    args = parser.parse_args()

    products = json.loads(DATA_FILE.read_text())
    on_sale = sum(is_on_sale(p) for p in products)
    transform(products)
    print(f"Loaded {len(products)} products; discounted {on_sale} in '{SALE_CATEGORY}'.")

    if args.dry_run:
        for p in [p for p in products if is_on_sale(p)][:5]:
            print(f"  {p['objectID']}: {p['price']:>5}  {p['name'][:60]}")
        return

    upload(products)


if __name__ == "__main__":
    main()
