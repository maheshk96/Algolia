# Spencer & Williams: Algolia Demo

**Live demo:** **bright-dango-5a02bd.netlify.app**

What I built for each part of the assignment, the decisions behind it, and how to run it. The original brief is in [BRIEF.md](BRIEF.md).

## Running it

Requires Node 20.19+ (see `.nvmrc`) and Python 3.9+.

```bash
cp .env.example .env               # add App ID, Search-Only key, index name, Admin key

pip install -r requirements.txt
python scripts/upload_products.py   # Part 1: transform + upload (--dry-run to preview)
python scripts/configure_index.py   # Part 3: relevance settings (--dry-run to preview)

npm install && npm start            # front end on http://localhost:3000
```

The Admin key is only read by the Python scripts. Only the App ID, Search-Only key and index name reach the browser.

## Part 1: Camera sale

[`scripts/upload_products.py`](scripts/upload_products.py) takes 20% off every product in the camera category, rounds down to a whole number, and uploads all 10,000 records in one run.

- **Which products count as "cameras".** The brief's "camera category" could mean several things in this data, so I asked before building. We chose the top-level category `Cameras & Camcorders` (753 products). It includes accessories such as memory cards and binoculars. Security cameras sit under "Connected Home" in this data, so they aren't included.
- **Rounding.** Prices are calculated with exact decimal arithmetic, so a value like 79.99999 can't wrongly round down to 79.
- **`price_range`.** This field is used for filtering by price. 98 products would have stayed in the wrong band after the discount, so the script recalculates it to keep price filters accurate.

## Part 2: Insights events

| User action | Event |
|---|---|
| Clicks a product card or **View** | `Product Clicked` (click after search) |
| Clicks **Add To Cart** | `Product Added To Cart` (conversion after search, `addToCart` subtype, with price) |
| Results load | `Hits Viewed` (automatic) |
| Applies a brand or category filter | `Filter Applied` (automatic) |

- Enabled with InstantSearch's built-in `insights` option. Every search then includes `clickAnalytics` and a `userToken`, so each event carries the `queryID` and the product's position in the results.
- The anonymous `userToken` is saved in a cookie so it stays the same between visits, which Personalization needs. In production this should only be set after the user consents to cookies.
- **Bug fixed:** the original CSS rule `.result-hit > * { pointer-events: none }` meant clicks on the buttons only ever registered on the card, so Add To Cart could never send a conversion.
- Add To Cart doesn't also count as a click, so clicks aren't double-counted. The add-to-cart event includes the price, so revenue appears in Analytics. Currency is set to USD because the data comes from Best Buy in the US.

## Part 3: Relevance

Settings live in [`scripts/configure_index.py`](scripts/configure_index.py), so they can be reviewed and re-run.

- **Searchable attributes:** name → brand → categories → type → description. The description is last because it's long and noisy. Attributes are `unordered`, because every name starts with "Brand - …" and a word's position doesn't indicate relevance.
- **Facets:** `brand` and `categories`, which the UI uses, plus `type`. These are also the signals Personalization can learn from.
- **Custom ranking:** `desc(rating)`.

**Data issue to raise with the customer:** `popularity` is not a real popularity signal. It equals each product's position in a file sorted alphabetically by name, so ranking on it would favour brands starting with "A". I left it out. The next step would be to get real sales data from Spencer & Williams, and meanwhile let Dynamic Re-Ranking and Personalization learn from the Part 2 events.

## Customer questions

Answers are in [questions/answers.md](questions/answers.md).

## Next steps I'd suggest

- Configure a Personalization strategy (events + `brand`/`categories`/`type`), then add `enablePersonalization: true` to searches once enough events have been collected.
- Turn on Dynamic Re-Ranking once there is enough click data.
- Send add-to-cart and purchase events from the product detail and checkout pages too.
