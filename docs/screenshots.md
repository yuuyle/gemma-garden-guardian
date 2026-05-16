# Screenshot Capture Guide

Use these screenshots for the README, Kaggle writeup, and video thumbnail material.

## Start The App

```bash
streamlit run app.py
```

For low-cost repeated captures, keep:

```text
GEMMA_GARDEN_MODE=mock
```

For one proof screenshot with real Gemma 4:

```text
GEMMA_GARDEN_MODE=vertex
GOOGLE_CLOUD_LOCATION=global
```

## Suggested Browser Setup

- Desktop viewport: 1440 x 1000 or similar
- Browser zoom: 100%
- Hide bookmarks bar if it distracts from the app
- Use `sample_data/images/tomato_web/05_tomato_fruiting.jpg` for the main demo

## Required Screenshots

Save screenshots under:

```text
assets/screenshots/
```

Suggested files:

| File | What to Capture |
|---|---|
| `01_home_upload.png` | App open with upload form and sample image preview |
| `02_dashboard_mock.png` | Mock analysis dashboard with risk score and todos |
| `03_history_report.png` | Sidebar history and weekly report expanded |
| `04_structured_json.png` | Structured JSON expander open |
| `05_vertex_result.png` | One real Gemma 4 result, if credentials and budget allow |
| `06_sample_images.png` | Finder or app view showing the tomato sample set |

## Demo Flow For Screenshots

1. Open the app.
2. Upload `sample_data/images/tomato_web/05_tomato_fruiting.jpg`.
3. Enter crop type: `tomato`.
4. Add notes: `Several fruits are visible. Please check visible leaf and fruit condition cautiously.`
5. Click **Analyze crop photo**.
6. Capture the dashboard.
7. Open **Structured JSON** and capture it.
8. Run a second sample such as `08_tomato_blurry_derived.jpg`.
9. Capture the history panel and weekly report.

## Safety Review Before Publishing

- Make sure no `.env` values, project IDs, tokens, or emails are visible.
- If using real Vertex mode, crop or blur any sensitive Cloud project information.
- Do not imply the app definitively diagnoses plant disease.
