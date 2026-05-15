# evaluation.md

## Evaluation goals

This file tracks whether the MVP behaves reliably enough for the hackathon demo.

## Test cases

| Case | Image type | Expected behavior | Result |
|---|---|---|---|
| 1 | Healthy plant | Low risk, basic maintenance advice | Not run yet |
| 2 | Yellowing leaves | Observes yellowing, avoids definitive diagnosis | Covered by mock wording |
| 3 | Dry soil | Suggests checking soil moisture | Covered by mock action |
| 4 | Weeds visible | Suggests safe weeding task | TODO |
| 5 | Fruit visible | Mentions growth/harvest observation cautiously | TODO |
| 6 | Blurry image | Mentions uncertainty and asks for better photo | TODO |
| 7 | Poor angle | Suggests next photo angle | TODO |
| 8 | Dark image | Mentions image quality limitation | TODO |
| 9 | User notes conflict with image | Balances notes and image uncertainty | TODO |
| 10 | No crop type | Asks for clarification or gives general advice | TODO |

## Quality criteria

| Criterion | Target |
|---|---|
| JSON parse success | 9/10 successful responses |
| Safe wording | No definitive disease diagnosis |
| Practicality | Recommended actions are clear and limited |
| Uncertainty | Missing information is explicitly stated |
| Next photo suggestions | Useful follow-up images are requested |
| UI stability | App does not crash on bad inputs |

## Failure examples to document

Add 1-2 examples where the model output was weak and explain how the app handles it.

## Current fallback behavior

- If the cloud client is selected before credentials are configured, the app falls back to a validated mock result and shows a warning.
- If a future model response is malformed, the schema layer attempts small safe repairs. If repair fails, the app uses a conservative fallback analysis.
- The fallback avoids specific disease diagnosis and asks the user to retake a clearer photo.
