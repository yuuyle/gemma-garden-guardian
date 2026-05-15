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

- [ ] Implement `src/gemma_client.py`
- [ ] Support mock mode via environment variable
- [ ] Add Google Cloud configuration notes
- [ ] Add API error handling
- [ ] Add JSON validation
- [ ] Add retry or fallback behavior

## Phase 4: Tool layer

- [ ] Implement `log_observation()`
- [ ] Implement `create_todo_items()`
- [ ] Implement `calculate_risk_score()`
- [ ] Implement `generate_weekly_report()`
- [ ] Save observations to JSONL

## Phase 5: Demo quality

- [ ] Add sample images
- [ ] Add history panel
- [ ] Add previous observation comparison
- [ ] Add screenshots
- [ ] Add architecture diagram
- [ ] Add `evaluation.md`

## Phase 6: Submission

- [ ] Finish README
- [ ] Finish Kaggle writeup draft
- [ ] Finish video script
- [ ] Record 3-minute demo
- [ ] Publish GitHub repository
- [ ] Deploy live demo if possible
- [ ] Submit to Kaggle

## Current priority

Phase 1 and Phase 2 are complete. Next priority is Phase 3 and Phase 4.

The first milestone is:

```text
streamlit run app.py
```

The app should open, accept an image, and display a mock structured analysis result without requiring Google Cloud credentials.
