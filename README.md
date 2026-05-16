# Gemma Garden Guardian

**An AI field assistant for small-scale growers powered by Gemma 4.**

Gemma Garden Guardian is a Streamlit demo for Kaggle's "The Gemma 4 Good Hackathon". It helps gardeners and small-scale growers upload a crop photo, add context, and receive a cautious structured analysis with visible observations, possible risks, recommended next actions, uncertainty, and follow-up photo suggestions.

The MVP runs in mock mode by default for low-cost development, and it can call Gemma 4 MaaS on Vertex AI when Google Cloud credentials are configured.

## MVP Features

- Streamlit web UI
- Crop or garden image upload
- Crop type input
- User notes input
- Mock structured analysis result
- Real Gemma 4 MaaS mode through Vertex AI
- JSON schema definition and validation
- Dashboard for summary, risk level, observations, possible issues, and action todos
- JSONL observation history
- Risk score and previous-observation comparison
- Weekly report summary from recent observations
- Web-collected tomato sample image set with attribution
- Safety-first wording that avoids definitive plant disease diagnosis

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in your terminal, upload a crop photo, add optional crop context, and click **Analyze crop photo**.

## Configuration

Copy the example environment file if you want to prepare for future Google Cloud integration:

```bash
cp .env.example .env
```

The app defaults to mock mode:

```text
GEMMA_GARDEN_MODE=mock
```

Observation logs are saved locally to:

```text
data/observations.jsonl
```

This log file is ignored by Git so demo data does not accidentally get committed.

## Google Cloud Notes

Mock mode is best for repeated development and recording takes. Vertex mode calls Gemma 4 MaaS through the Google Gen AI SDK.

Cloud mode uses:

```text
GEMMA_GARDEN_MODE=vertex
GOOGLE_CLOUD_PROJECT=<your-project-id>
GOOGLE_CLOUD_LOCATION=global
GEMMA_MODEL_ID=gemma-4-26b-a4b-it-maas
```

For the preferred Gemma 4 MaaS model, Google may require the `global` endpoint. The client will also retry once with `global` if a regional endpoint returns that specific error.

Do not commit `.env`, service account JSON files, API keys, or other secrets.

## Deployment

Cloud Run deployment files are included:

```text
Dockerfile
docs/DEPLOYMENT.md
```

For public demos, deploy in mock mode first, then switch to `vertex` mode only when you want to demonstrate the real Gemma 4 call.

## Submission Assets

- Kaggle writeup draft: `docs/kaggle_writeup_draft.md`
- Video script: `docs/video_script.md`
- Screenshot guide: `docs/screenshots.md`
- Architecture diagram: `assets/architecture_diagram.png`
- Sample image attribution: `sample_data/images/tomato_web/ATTRIBUTION.md`

## Responsible Use

This is not a plant disease diagnosis tool. The app describes visible signs, possible risks, and practical next steps using cautious wording such as "may indicate" and "visible signs suggest". For high-risk decisions, users should confirm locally and consider consulting an agricultural extension service or local expert.

The app does not recommend specific pesticide usage. Any pesticide-related decisions should follow local regulations and product labels.

## Sample Images

The repository includes a small tomato sample set for mock demos and evaluation:

```text
sample_data/images/tomato_web/
```

The set covers whole plant, leaf close-up, soil condition, weeds/context, fruiting, dry-looking, healthy-looking, blurry, dark, and poor-angle cases. Attribution and licenses are recorded in:

```text
sample_data/images/tomato_web/ATTRIBUTION.md
sample_data/images/tomato_web/manifest.json
```

See `docs/sample_images.md` for details. Some difficult photo-quality cases are derived from licensed Wikimedia Commons images and are marked as derived.

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
  data/
    observations.jsonl
  docs/
  assets/
```

## Next Milestones

- Capture app screenshots
- Record a 3-minute demo video
- Submit the GitHub URL, video URL, and writeup to Kaggle
