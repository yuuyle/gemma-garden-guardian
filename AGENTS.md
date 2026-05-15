# AGENTS.md

## Project

This repository is for Kaggle's "The Gemma 4 Good Hackathon".

Project name:

**Gemma Garden Guardian**

Subtitle:

**An AI field assistant for small-scale growers powered by Gemma 4.**

## Goal

Build a working demo application that helps small-scale growers and home gardeners analyze crop photos, understand visible risks, and generate safe, practical next actions.

The project must be completed for Kaggle submission. Prioritize a working MVP, clear demo, README, video script, and Kaggle writeup over adding extra features.

## Core concept

Users upload a crop or garden photo, optionally enter crop type and notes, and the app sends the image and context to Gemma 4 on Google Cloud.

Gemma 4 returns structured JSON with:

- visible observations
- overall crop status
- risk level
- possible issues
- recommended actions
- uncertainty
- next photo suggestions

The app then converts that JSON into a dashboard with todos, risk summary, logs, and a simple report.

## Technical direction

Use Google Cloud / Vertex AI / Model Garden Gemma 4 instead of local LLM execution.

The user's local PC is not powerful enough to run Gemma 4 locally. Do not design the MVP around Ollama, llama.cpp, local GPU, or Raspberry Pi inference.

Preferred model:

```text
gemma-4-26b-a4b-it-maas
```

Required app stack:

- Python
- Streamlit
- Google Cloud authentication
- JSON schema validation
- JSONL or SQLite logging
- Mock mode for development without API calls

## Must-have MVP features

1. Streamlit UI
2. Image upload
3. Crop type input
4. User notes input
5. Gemma 4 API call
6. Structured JSON output
7. JSON validation and repair/fallback handling
8. Observation dashboard
9. Recommended action todos
10. Observation log saved to JSONL or SQLite
11. Sample images
12. README with setup instructions
13. Kaggle writeup draft
14. Video script draft

## Should-have features

1. Previous observation comparison
2. Risk score display
3. Weekly report generation
4. Cloud Run deployment
5. Architecture diagram
6. Evaluation table using sample images

## Do not prioritize

- Fine-tuning
- Local LLM inference
- Raspberry Pi integration
- YOLO or custom CV model training
- Production-grade plant disease diagnosis
- Specific pesticide instructions
- Complex RAG infrastructure

## Safety and wording rules

This is not a plant disease diagnosis tool.

The app must avoid overconfident statements. Use wording such as:

- "may indicate"
- "visible signs suggest"
- "please confirm by checking..."
- "consider consulting a local expert"

Do not make definitive disease or pest diagnoses from a single image.

Do not recommend specific pesticide usage. If pesticide-related guidance appears, tell users to follow local regulations and product labels.

## Expected repository structure

```text
gemma-garden-guardian/
  README.md
  app.py
  requirements.txt
  .env.example
  .gitignore
  AGENTS.md

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
    HANDOFF.md
    TASKS.md
    ARCHITECTURE.md
    DECISIONS.md
    KAGGLE_SUBMISSION_CHECKLIST.md
    kaggle_writeup_draft.md
    video_script.md
    evaluation.md
    cost_notes.md

  assets/
    screenshots/
    architecture_diagram.png
```

## Development rules

- Keep the app runnable at all times.
- Prefer simple, reliable code over complex architecture.
- Add mock mode before real API integration.
- Never commit `.env`, API keys, service account JSON, or secrets.
- Update `docs/TASKS.md` after completing tasks.
- Update `docs/DECISIONS.md` when making architectural decisions.
- Run basic tests or at least `python -m compileall .` before committing.
- For each implementation step, explain what changed and what remains.

## Final submission targets

The final Kaggle submission should include:

- Public GitHub repository
- Live demo URL if possible
- 3-minute video URL
- Kaggle writeup, ideally under 1,500 words
- Screenshots
- Architecture diagram
