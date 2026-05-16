# Gemma Garden Guardian: An AI Field Assistant for Small-Scale Growers

## Problem

Small-scale growers and home gardeners often notice crop problems too late. Yellowing leaves, dry soil, weeds, pest-like signs, poor photo quality, and uncertain harvest timing can be difficult to interpret, especially for beginners or people without easy access to local experts.

This project explores how Gemma 4 can help people observe their gardens more carefully and take safer next actions.

## Who it helps

Gemma Garden Guardian is designed for:

- home gardeners
- small-scale farmers
- community garden users
- beginners
- elderly growers
- people with limited access to expert agricultural advice

## What we built

Gemma Garden Guardian is a photo-based AI field assistant built with Python and Streamlit.

Users upload a crop or garden photo, enter the crop type and optional notes, and receive a structured analysis with:

- visible observations
- possible risks
- risk level
- recommended actions
- uncertainty
- next photo suggestions

The app also logs observations and converts recommended actions into simple todos.

## How Gemma 4 is used

The project uses Gemma 4 through Google Cloud / Vertex AI MaaS rather than local inference. This keeps the demo practical on ordinary hardware while still showing multimodal Gemma 4 usage.

Gemma 4 is used for:

- multimodal crop photo understanding
- combining image and text notes
- generating structured JSON output
- supporting a tool-style local workflow
- providing input for local logging, todo generation, risk scoring, and reporting
- producing uncertainty-aware recommendations

Preferred model:

```text
gemma-4-26b-a4b-it-maas
```

## System architecture

```text
User
  ↓
Streamlit Web App
  ↓
Image + Crop Type + Notes
  ↓
Gemma 4 26B A4B IT MaaS
  ↓
Structured JSON
  ↓
Tool Layer
  ├─ log_observation()
  ├─ create_todo_items()
  ├─ calculate_risk_score()
  └─ generate_weekly_report()
  ↓
Garden Dashboard
```

## Technical implementation

The app is built with Python and Streamlit.

Key implementation elements:

- image upload UI
- mock mode for low-cost development
- real Gemma 4 MaaS mode using the Google Gen AI SDK
- JSON schema validation
- JSON repair/fallback behavior
- JSONL observation logging
- todo generation from recommended actions
- risk score and previous observation comparison
- weekly report generation
- sample tomato images with attribution
- safe output wording

The app asks Gemma 4 for a JSON object with visible observations, possible risks, recommended actions, uncertainty, and next photo suggestions. The local app validates the JSON before displaying it. If the cloud request fails or the model output cannot be validated, the app falls back to a conservative response instead of crashing.

## Responsible use

This app is not a plant disease diagnosis tool. It does not replace local agricultural experts.

The app avoids definitive claims and uses uncertainty-aware language such as:

- "visible signs suggest"
- "may indicate"
- "please confirm"
- "consider consulting a local expert"

It does not provide specific pesticide instructions.

For high-risk decisions, users should confirm by checking the plant in person and consider local agricultural advice.

## Impact and future vision

Gemma Garden Guardian can help small-scale growers act earlier, learn from repeated observations, and reduce avoidable crop loss.

Future improvements could include:

- sensor CSV integration
- local crop adaptation
- Cloud Run public deployment
- stronger evaluation across more crop types
- region-specific gardening guidance
- community garden monitoring workflows
