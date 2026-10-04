"""Shared helper: builds an Algolia client from the repo's .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def get_client_and_index():
    from algoliasearch.search.client import SearchClientSync

    load_dotenv(ENV_FILE)
    required = ["ALGOLIA_APP_ID", "ALGOLIA_ADMIN_API_KEY", "ALGOLIA_INDEX"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"Missing {', '.join(missing)}. Add them to {ENV_FILE} (see .env.example).")

    # Admin key: write access needed; never ship this to the front end.
    client = SearchClientSync(os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_ADMIN_API_KEY"])
    return client, os.environ["ALGOLIA_INDEX"]
