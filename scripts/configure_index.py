"""
Part Three: Relevance configuration.

Applies the index settings so shoppers see the results that make most sense.
Keeping them in code makes them reviewable and repeatable across environments.

Usage:
    python scripts/configure_index.py            # apply settings
    python scripts/configure_index.py --dry-run  # print settings only
"""

import argparse
import json

from algolia_client import get_client_and_index

SETTINGS = {
    # Where to look for the query, most important first. A match in the product name beats a
    # match in the brand, which beats categories and product type. The description is long and
    # noisy, so it comes last. unordered() means a word's position inside the attribute doesn't
    # matter: names all start with "Brand - ...", so word position says nothing useful.
    "searchableAttributes": [
        "unordered(name)",
        "brand",
        "unordered(categories)",
        "type",
        "unordered(description)",
    ],
    # Facets the UI filters on (brand, categories). They are also the signals Personalization
    # learns from, along with type. searchable() lets shoppers search inside long facet lists.
    "attributesForFaceting": [
        "searchable(brand)",
        "searchable(categories)",
        "type",
    ],
    # Business tie-breaker, applied only between results that are equally relevant to the text.
    # `popularity` is deliberately left out: in the supplied data it is just each product's
    # position in an alphabetically sorted file, so it would favour brands starting with "A".
    "customRanking": ["desc(rating)"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print settings, do not apply")
    args = parser.parse_args()

    print(json.dumps(SETTINGS, indent=2))
    if args.dry_run:
        return

    client, index_name = get_client_and_index()
    response = client.set_settings(index_name, SETTINGS)
    client.wait_for_task(index_name, response.task_id)
    print(f"Applied settings to '{index_name}'.")


if __name__ == "__main__":
    main()
