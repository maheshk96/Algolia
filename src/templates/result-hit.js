const CURRENCY = 'USD';

/**
 * Hit template for the results page.
 *
 * Insights events (queryID and position are added automatically by InstantSearch):
 * - Clicking the card or "View" sends a click event.
 * - "Add To Cart" sends an addToCart conversion event with the price, so revenue shows in Analytics.
 *
 * @param {object} hit - Algolia hit.
 * @param {object} helpers - InstantSearch template helpers.
 * @param {Function} helpers.html - Tagged template for rendering.
 * @param {object} helpers.components - Built-in components (Highlight, Snippet...).
 * @param {Function} helpers.sendEvent - Sends Insights events for this hit.
 * @returns {object} Rendered template.
 */
const resultHit = (hit, { html, components, sendEvent }) => {
  const addToCart = (event) => {
    // Stop the card's click handler also firing: adding to cart is a conversion, not a click.
    event.stopPropagation();
    sendEvent('conversion', hit, 'Product Added To Cart', {
      eventSubtype: 'addToCart',
      objectData: [{ price: hit.price, quantity: 1 }],
      value: hit.price,
      currency: CURRENCY,
    });
  };

  // eslint-disable-next-line new-cap -- InstantSearch component helper, not a constructor
  const name = components.Highlight({ hit, attribute: 'name' });

  return html`<a class="result-hit" onClick=${() => sendEvent('click', hit, 'Product Clicked')}>
    <div class="result-hit__image-container">
      <img class="result-hit__image" src="${hit.image}" />
    </div>
    <div class="result-hit__details">
      <h3 class="result-hit__name">${name}</h3>
      <p class="result-hit__price">$${hit.price}</p>
    </div>
    <div class="result-hit__controls">
      <button class="result-hit__view">View</button>
      <button class="result-hit__cart" onClick=${addToCart}>Add To Cart</button>
    </div>
  </a>`;
};

export default resultHit;
