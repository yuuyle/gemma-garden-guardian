# ARCHITECTURE.md

## Overview

Gemma Garden Guardian is a lightweight web application that helps small-scale growers and home gardeners analyze crop photos and convert visible observations into safe next actions.

The MVP uses Google Cloud-hosted Gemma 4 instead of local inference.

## High-level architecture

```text
User
  ↓
Streamlit Web App
  ↓
Image + Crop Type + Notes
  ↓
Gemma 4 26B A4B IT MaaS on Google Cloud
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

## Components

### 1. Streamlit Web App

Responsible for:

- image upload
- crop type input
- user notes input
- result dashboard
- history display
- demo-friendly UI

### 2. Gemma Client

Responsible for:

- preparing image and text input
- calling Gemma 4 on Google Cloud
- enforcing structured output
- handling API errors
- supporting mock mode

Expected file:

```text
src/gemma_client.py
```

### 3. Prompt Layer

Responsible for:

- system instructions
- safety wording
- JSON output instructions
- gardening context
- previous observation context

Expected file:

```text
src/prompts.py
```

### 4. Schema Layer

Responsible for:

- JSON schema definition
- validation
- graceful fallback if response is malformed

Expected file:

```text
src/schemas.py
```

### 5. Tool Layer

Responsible for:

- saving observations
- creating todos
- calculating risk score
- generating reports

Expected file:

```text
src/tools.py
```

### 6. Storage Layer

MVP storage can be JSONL.

Expected path:

```text
data/observations.jsonl
```

Future storage can be SQLite.

Current MVP implementation:

- `GEMMA_GARDEN_MODE=mock` is the default and requires no credentials.
- `GEMMA_GARDEN_MODE=vertex` calls Gemma 4 MaaS through the Google Gen AI SDK.
- The preferred Gemma 4 MaaS model may require the `global` endpoint, so the client retries once with `global` if a regional endpoint returns that specific error.
- Observations are saved to `data/observations.jsonl`.
- The architecture diagram is available at `assets/architecture_diagram.png`.
- The editable SVG source is available at `assets/architecture_diagram.svg`.

## Data flow

1. User uploads image.
2. User enters crop type and optional notes.
3. App builds prompt with safety rules and expected JSON schema.
4. App sends image + text to Gemma 4.
5. Gemma 4 returns JSON.
6. App validates JSON.
7. App executes local tool functions.
8. App displays dashboard and saves log.

## Safety design

The app must not claim to diagnose plant diseases definitively.

The app should use wording like:

- may indicate
- visible signs suggest
- please confirm
- consider consulting a local expert

The app should avoid specific pesticide instructions.

## Deployment options

Preferred:

- Cloud Run + Streamlit app
- Gemma 4 26B MaaS API call

Alternative:

- Hugging Face Spaces
- Streamlit Community Cloud
- local demo recording only

## MVP boundary

The MVP does not include:

- local LLM inference
- fine-tuning
- custom CV training
- Raspberry Pi integration
- production-grade disease diagnosis
