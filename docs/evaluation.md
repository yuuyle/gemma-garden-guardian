# evaluation.md

## Evaluation goals

This file tracks whether the MVP behaves reliably enough for the hackathon demo.

## Test cases

Use the sample set in `sample_data/images/tomato_web/` for the first evaluation pass.

| Case | Image type | Expected behavior | Result |
|---|---|---|---|
| 1 | Healthy plant | Low risk, basic maintenance advice | Sample available |
| 2 | Leaf close-up | Observes visible leaf condition, avoids definitive diagnosis | Sample available |
| 3 | Soil condition | Suggests checking soil moisture | Sample available |
| 4 | Weeds visible | Suggests safe weeding task | Sample available |
| 5 | Fruit visible | Mentions growth/harvest observation cautiously | Sample available |
| 6 | Dry-looking/water-stress-like | Suggests checking soil moisture before watering | Derived sample available |
| 7 | Blurry image | Mentions uncertainty and asks for better photo | Derived sample available |
| 8 | Dark image | Mentions image quality limitation | Derived sample available |
| 9 | Poor angle | Suggests next photo angle | Derived sample available |
| 10 | No crop type | Gives general advice without overclaiming | App input case |

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
