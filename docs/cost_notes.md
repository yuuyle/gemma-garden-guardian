# cost_notes.md

## Cost strategy

The MVP uses Google Cloud-hosted Gemma 4 instead of local inference.

This may incur API usage costs. The app should be designed to reduce unnecessary calls during development and demos.

## Cost-saving measures

- Use mock mode by default during development.
- Only call Gemma 4 when explicitly requested.
- Cache results for repeated demo inputs if practical.
- Limit image size before sending.
- Limit history context length.
- Keep sample demo runs small.
- Set Google Cloud budget alerts.

## Suggested budget alerts

Set Google Cloud budget alerts at:

- 500 JPY
- 1,000 JPY
- 2,000 JPY

## Avoid

Do not deploy a persistent custom GPU endpoint for this MVP unless absolutely necessary.

Do not leave paid compute resources running after testing.
