# Customer Question Answers

## Question 1

**To:** marissa@startup.com
**Subject:** Re: Bad design

Hi Marissa,

Thanks for telling us. This is exactly the feedback we want to hear, and I've passed it on to our product team along with your use case of clearing and deleting indices often while iterating.

In the meantime, here are two quicker ways to do this that skip the dashboard entirely:

- **Algolia CLI:** `algolia indices clear <index> -y` empties an index, and `algolia indices delete <index> -y` removes it (add `--include-replicas` to remove its replicas too).
- **API clients:** `clearObjects` and `deleteIndex` are available in all our client libraries, so you can reset an index as part of your build or test script.

If you're re-uploading data each time, `replaceAllObjects` swaps in the new data in one step, so you don't need to clear the index first.

Let me know if you'd like a hand setting either of these up.

Best,
Mahesh

---

## Question 2

**To:** carrie@coffee.com
**Subject:** Re: URGENT ISSUE WITH PRODUCTION!!!!

Hi Carrie,

I'm sorry for the disruption. Let's get your reviews publishing again.

**What's happening:** every Algolia record has a maximum size, between 10 KB and 100 KB depending on your plan. This limit applies to every account, so it isn't a billing or account issue. Since this morning, some records have gone over that size and Algolia is rejecting them. That's most likely a long review combined with the extra metadata you add to each record.

**How to fix it:**

1. **Send Algolia only what you need for search, display and ranking.** Keep the rest of the metadata in your own database and look it up by `objectID` when a page is shown. This is the quickest fix, and it usually shrinks records a lot.
2. **Split very long reviews into several smaller records**, for example one per paragraph, all sharing a `shop_id`. Then set `attributeForDistinct: "shop_id"` with `distinct: true` so each coffee shop still appears once in the results.
3. If you still need bigger records after that, we can talk about a plan with a higher limit.

**One thing worth checking:** the error is appearing in your users' browsers, which suggests reviews may be sent to Algolia directly from the front end. If so, an API key with write access is visible in your site's code, and anyone could use it to change or delete your data. I'd recommend sending records from your server instead and using a search-only key in the browser.

Could you send me your App ID, the `objectID` of a review that failed, and anything that changed around 9:15am (a deploy or new metadata fields)? That will let me confirm the cause quickly. I'm also happy to jump on a call.

Best,
Mahesh

---

## Question 3

**To:** marc@hotmail.com
**Subject:** Re: Error on website

Hi Marc,

Thanks for sending the screenshot. That makes this much quicker to track down.

**What the error means:** your site's JavaScript uses something called `searchkit` on the first line of `index.js`, but it was never loaded or defined. The browser stops at that point, so the rest of the page doesn't run.

**What's most likely causing it:**

- **The library isn't installed or imported.** Check that `searchkit` is listed in your `package.json` and imported at the top of `index.js`, then rebuild your site.
- **A spelling or capitalisation mismatch.** JavaScript is case-sensitive, so `Searchkit` and `searchkit` are different names. Check that the name you use matches the one you imported.

**One thing to check:** Searchkit is a separate open-source library for searching with Elasticsearch, and it isn't part of Algolia. If you meant to use Algolia, you'd use our `algoliasearch` and InstantSearch libraries instead. I'm happy to point you to a short getting-started guide.

If that doesn't sort it out, could you send me the first few lines of your `index.js`, your `package.json`, and your website's address? I'll take a look straight away.

Best,
Mahesh
