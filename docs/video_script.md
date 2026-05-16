# Video Script

Target length: approximately 3 minutes.

## 0:00 - 0:20 - Problem

"Small-scale growers and home gardeners often spot changes in their plants before they know what those changes mean.

A few yellow leaves, dry soil, weeds, or a blurry nighttime photo can be hard to interpret, especially for beginners or people without quick access to local experts."

## 0:20 - 0:45 - Vision

"This is Gemma Garden Guardian: an AI field assistant for small-scale growers, powered by Gemma 4.

The goal is not to replace farmers or plant experts. The goal is to help people observe more carefully, act earlier, and make safer next decisions."

## 0:45 - 1:40 - Demo

Show the Streamlit app.

1. Upload a tomato or garden photo.
2. Enter crop type.
3. Add optional notes.
4. Click analyze.
5. Show the dashboard:
   - summary
   - observations
   - risk score
   - possible risks
   - recommended actions
   - uncertainty
   - next photo suggestions
6. Show todos, structured JSON, history, and weekly report.

Narration:

"Here I upload a tomato photo, enter the crop type, and add a short note. Gemma 4 reads the image and text together, then returns a structured JSON response.

The app validates that JSON before showing it. Instead of giving a definitive diagnosis, it describes visible signs, possible risks, uncertainty, and practical next actions. Those actions become simple todos, and the observation is saved to a local JSONL history."

## 1:40 - 2:20 - Technical Explanation

"The app is built with Python and Streamlit. It uses mock mode by default so development and video recording stay cheap and reliable.

When cloud mode is enabled, the app calls Gemma 4 MaaS through Vertex AI using the Google Gen AI SDK. The request includes the image, crop type, notes, and a strict JSON output instruction.

The local tool layer validates the JSON, creates todos, calculates a simple risk score, saves observations to JSONL, and generates a weekly report. If the API fails or the JSON is malformed, the app falls back safely instead of crashing."

Key technical elements:

- Gemma 4 multimodal input
- crop image plus user notes
- structured JSON output
- local tool-style workflow
- observation logging
- safe, uncertainty-aware recommendations

Architecture:

```text
User → Streamlit → Gemma 4 → JSON → Tool Layer → Garden Dashboard
```

## 2:20 - 2:45 - Impact

"This can help home gardeners, small-scale growers, community gardens, elderly growers, and people with limited expert access.

The impact is not just faster answers. It is helping people build a habit of better observation: taking clearer photos, checking soil moisture, comparing history, and knowing when to ask a local expert."

## 2:45 - 3:00 - Closing

"Gemma Garden Guardian turns everyday garden photos into safer, clearer next actions.

AI should not replace growers. It should help them observe, learn, and act with confidence."
