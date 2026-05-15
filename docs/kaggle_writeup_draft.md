# Kaggle Writeup Draft

# Gemma Garden Guardian: An AI Field Assistant for Small-Scale Growers

## Problem

Small-scale growers and home gardeners often notice changes in their crops too late. Yellowing leaves, dry soil, weeds, pests, poor image conditions, and uncertain harvest timing can be difficult to interpret, especially for beginners or people without access to local experts.

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

Gemma Garden Guardian is a photo-based AI field assistant.

Users upload a crop or garden photo, enter the crop type and optional notes, and receive a structured analysis with:

- visible observations
- possible risks
- risk level
- recommended actions
- uncertainty
- next photo suggestions

The app also logs observations and converts recommended actions into simple todos.

## How Gemma 4 is used

The project uses Gemma 4 through Google Cloud rather than local inference.

Gemma 4 is used for:

- multimodal crop photo understanding
- combining image and text notes
- generating structured JSON output
- supporting a function-calling-style tool workflow
- summarizing previous observations
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
- Gemma 4 client
- JSON schema validation
- JSONL observation logging
- todo generation from recommended actions
- safe output wording
- optional previous observation comparison

## Responsible use

This app is not a plant disease diagnosis tool. It does not replace local agricultural experts.

The app avoids definitive claims and uses uncertainty-aware language such as:

- "visible signs suggest"
- "may indicate"
- "please confirm"
- "consider consulting a local expert"

It does not provide specific pesticide instructions.

## Impact and future vision

Gemma Garden Guardian can help small-scale growers act earlier, learn from repeated observations, and reduce avoidable crop loss.

Future improvements could include:

- sensor CSV integration
- local crop adaptation
- offline Gemma deployment on edge devices
- fine-tuning for region-specific crops
- community garden monitoring workflows
