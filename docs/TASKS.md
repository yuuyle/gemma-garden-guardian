# TASKS.md

## Phase 1: Project skeleton

- [x] Create repository structure
- [x] Create README.md
- [x] Create AGENTS.md
- [x] Create .env.example
- [x] Create requirements.txt
- [x] Create app.py with minimal Streamlit app
- [x] Add mock analysis result

## Phase 2: Core app

- [x] Implement image upload UI
- [x] Implement crop type input
- [x] Implement notes input
- [x] Implement result dashboard
- [x] Implement JSON schema in `src/schemas.py`
- [x] Implement mock response in `src/sample_outputs.py`

## Phase 3: Gemma 4 integration

- [x] Implement `src/gemma_client.py`
- [x] Support mock mode via environment variable
- [x] Add Google Cloud configuration notes
- [x] Add API error handling
- [x] Add JSON validation
- [x] Add retry or fallback behavior
- [x] Implement real Vertex AI / Gemma 4 MaaS API request
- [x] Parse real Gemma 4 response into JSON
- [x] Test `GEMMA_GARDEN_MODE=vertex`

## Phase 4: Tool layer

- [x] Implement `log_observation()`
- [x] Implement `create_todo_items()`
- [x] Implement `calculate_risk_score()`
- [x] Implement `generate_weekly_report()`
- [x] Save observations to JSONL

## Phase 5: Demo quality

- [x] Add sample images
- [x] Add history panel
- [x] Add previous observation comparison
- [ ] Add screenshots
- [x] Add architecture diagram
- [x] Add `evaluation.md`
- [x] Add screenshot capture guide

## Phase 6: Submission

- [x] Finish README
- [x] Finish Kaggle writeup draft
- [x] Finish video script
- [ ] Record 3-minute demo
- [x] Publish GitHub repository
- [x] Add Cloud Run deployment docs
- [ ] Deploy live demo if possible
- [ ] Submit to Kaggle

## Current priority

Phase 1 through Phase 4 are complete, including real Vertex AI / Gemma 4 MaaS smoke testing. Phase 5 is mostly complete; screenshots remain.

The first milestone is:

```text
streamlit run app.py
```

The app should open, accept an image, and display a mock structured analysis result without requiring Google Cloud credentials.

Next milestone:

```text
streamlit run app.py
```

Record screenshots and a short demo video. Use mock mode for cheap repeated takes, and vertex mode for one real Gemma 4 proof point.
