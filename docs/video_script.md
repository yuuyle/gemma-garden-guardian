# Video Script

Target length: approximately 3 minutes.

## 0:00 - 0:20 — Problem

Home gardeners and small-scale growers often notice crop problems too late.

A few yellow leaves, dry soil, new weeds, or unclear growth patterns can be hard to interpret, especially for beginners.

## 0:20 - 0:45 — Vision

Gemma Garden Guardian is an AI field assistant powered by Gemma 4.

The goal is not to replace farmers or experts. The goal is to help people observe better, act earlier, and grow with more confidence.

## 0:45 - 1:40 — Demo

Show the Streamlit app.

1. Upload a tomato or garden photo.
2. Enter crop type.
3. Add optional notes.
4. Click analyze.
5. Show Gemma 4 structured output:
   - summary
   - observations
   - risk level
   - recommended actions
   - uncertainty
   - next photo suggestions
6. Show todos generated from the recommendations.
7. Show observation log or previous comparison if implemented.

Narration:

"Gemma 4 looks at the image and the gardener's notes, then returns a structured JSON result. The app validates that result and turns it into practical next actions."

## 1:40 - 2:20 — Technical explanation

The MVP uses Google Cloud-hosted Gemma 4 instead of local inference because local hardware is limited.

Key technical elements:

- Gemma 4 multimodal input
- crop image plus user notes
- structured JSON output
- function-calling-style local tools
- observation logging
- safe, uncertainty-aware recommendations

Architecture:

```text
User → Streamlit → Gemma 4 → JSON → Tool Layer → Garden Dashboard
```

## 2:20 - 2:45 — Impact

This can help:

- home gardeners
- small-scale growers
- community gardens
- elderly growers
- people with limited expert access

It can support food resilience and digital equity by making basic crop observation more accessible.

## 2:45 - 3:00 — Closing

Gemma Garden Guardian helps people turn everyday garden photos into safer, clearer next actions.

AI should not replace growers. It should help them observe, learn, and act with confidence.
