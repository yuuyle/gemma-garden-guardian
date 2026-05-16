# Cloud Run Deployment

This guide deploys Gemma Garden Guardian to Cloud Run with Streamlit.

## Prerequisites

- Google Cloud project with billing enabled
- Vertex AI API enabled
- Cloud Run and Artifact Registry available
- Local `gcloud` CLI authenticated

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com
```

## Recommended Environment Variables

For a low-cost public demo, start with mock mode:

```text
GEMMA_GARDEN_MODE=mock
GOOGLE_CLOUD_LOCATION=global
GEMMA_MODEL_ID=gemma-4-26b-a4b-it-maas
```

For a real Gemma 4 demo:

```text
GEMMA_GARDEN_MODE=vertex
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
GEMMA_MODEL_ID=gemma-4-26b-a4b-it-maas
GEMMA_MAX_RETRIES=1
GEMMA_TEMPERATURE=0.1
GEMMA_MAX_OUTPUT_TOKENS=2048
```

Do not deploy `.env` files or service account JSON keys. Prefer the Cloud Run service identity.

## Deploy From Source

This is the simplest path:

```bash
gcloud run deploy gemma-garden-guardian \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars GEMMA_GARDEN_MODE=mock,GOOGLE_CLOUD_LOCATION=global,GEMMA_MODEL_ID=gemma-4-26b-a4b-it-maas
```

After the service is deployed, Cloud Run prints a public URL.

## Enable Real Gemma 4 Mode

First, identify the Cloud Run service account:

```bash
gcloud run services describe gemma-garden-guardian \
  --region asia-northeast1 \
  --format='value(spec.template.spec.serviceAccountName)'
```

Grant the service account permission to call Vertex AI:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member='serviceAccount:SERVICE_ACCOUNT_EMAIL' \
  --role='roles/aiplatform.user'
```

Then update environment variables:

```bash
gcloud run services update gemma-garden-guardian \
  --region asia-northeast1 \
  --set-env-vars GEMMA_GARDEN_MODE=vertex,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=global,GEMMA_MODEL_ID=gemma-4-26b-a4b-it-maas,GEMMA_MAX_RETRIES=1,GEMMA_TEMPERATURE=0.1,GEMMA_MAX_OUTPUT_TOKENS=2048
```

## Cost Controls

- Keep `GEMMA_GARDEN_MODE=mock` for repeated public demos.
- Switch to `vertex` only when demonstrating the real Gemma 4 call.
- Set budget alerts in Google Cloud Billing.
- Review Cloud Run logs after testing.
- Delete the service if you no longer need it:

```bash
gcloud run services delete gemma-garden-guardian --region asia-northeast1
```
