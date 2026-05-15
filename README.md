# Gemma Garden Guardian

**An AI field assistant for small-scale growers powered by Gemma 4.**

Gemma Garden Guardian is a Streamlit demo for Kaggle's "The Gemma 4 Good Hackathon". It helps gardeners and small-scale growers upload a crop photo, add context, and receive a cautious structured analysis with visible observations, possible risks, recommended next actions, uncertainty, and follow-up photo suggestions.

The current MVP runs in mock mode and does not require Google Cloud credentials.

## MVP Features

- Streamlit web UI
- Crop or garden image upload
- Crop type input
- User notes input
- Mock structured analysis result
- JSON schema definition and validation
- Dashboard for summary, risk level, observations, possible issues, and action todos
- Safety-first wording that avoids definitive plant disease diagnosis

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in your terminal, upload a crop photo, add optional crop context, and click **Analyze with mock Gemma response**.

## Configuration

Copy the example environment file if you want to prepare for future Google Cloud integration:

```bash
cp .env.example .env
```

The app defaults to mock mode:

```text
GEMMA_GARDEN_MODE=mock
```

Do not commit `.env`, service account JSON files, API keys, or other secrets.

## Responsible Use

This is not a plant disease diagnosis tool. The app describes visible signs, possible risks, and practical next steps using cautious wording such as "may indicate" and "visible signs suggest". For high-risk decisions, users should confirm locally and consider consulting an agricultural extension service or local expert.

The app does not recommend specific pesticide usage. Any pesticide-related decisions should follow local regulations and product labels.

## Project Structure

```text
.
  app.py
  requirements.txt
  .env.example
  src/
    gemma_client.py
    prompts.py
    schemas.py
    tools.py
    storage.py
    report.py
    sample_outputs.py
  sample_data/
    images/
    sensor_logs/
    examples.jsonl
  docs/
  assets/
```

## Next Milestones

- Add Google Cloud / Vertex AI Gemma 4 integration
- Save observations to JSONL
- Generate todos from recommended actions
- Add sample images, screenshots, and architecture diagram
- Finish Kaggle writeup and video script
