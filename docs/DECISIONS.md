# DECISIONS.md

This file records project decisions so Codex and future contributors can keep the project consistent.

## Decision 001: Use Google Cloud instead of local inference

### Status

Accepted

### Context

The user's local PC is not powerful enough to run Gemma 4 locally.

### Decision

Use Google Cloud / Vertex AI / Model Garden Gemma 4 for the MVP.

Preferred model:

```text
gemma-4-26b-a4b-it-maas
```

### Consequences

- Faster development
- No need for local GPU
- Easier to build a stable demo
- Some API cost is expected
- Local inference special tracks are not the main target

## Decision 002: Use Streamlit for the MVP

### Status

Accepted

### Context

The project needs a fast, demo-friendly UI for image upload and result display.

### Decision

Use Streamlit.

### Consequences

- Quick development
- Easy local demo
- Easy screenshot and video capture
- Not a polished production frontend, but sufficient for hackathon submission

## Decision 003: Start with mock mode

### Status

Accepted

### Context

Development should continue even before Google Cloud authentication is fully configured.

### Decision

Implement mock mode first.

### Consequences

- UI and tool layer can be built immediately
- API costs are reduced during development
- Demo can still show fallback behavior

## Decision 004: Use JSONL for initial logging

### Status

Accepted

### Context

The MVP needs simple observation history.

### Decision

Use JSONL initially.

Expected file:

```text
data/observations.jsonl
```

### Consequences

- Very simple implementation
- Easy to inspect
- Good enough for demo
- Can migrate to SQLite later

## Decision 005: Avoid definitive plant disease diagnosis

### Status

Accepted

### Context

The app uses photos and LLM reasoning. It should not overclaim.

### Decision

The app presents visible observations, possible risks, uncertainty, and safe next steps.

### Consequences

- Safer wording
- Better trust
- Clear limitations in README and writeup

## Decision 006: Keep Phase 1/2 schema validation lightweight

### Status

Accepted

### Context

The first milestone is a runnable Streamlit MVP that accepts an image and displays a mock structured analysis without requiring cloud credentials.

### Decision

Define the expected Gemma response shape in `src/schemas.py` using JSON Schema and validate the mock payload with `jsonschema`.

### Consequences

- The UI and mock data already exercise the same structure intended for Gemma 4 output
- Future repair and fallback logic can build on the same schema
- The implementation stays small enough for the hackathon MVP

## Decision 007: Build the 3-minute demo video as a replaceable HyperFrames composition

### Status

Accepted

### Context

The final Kaggle submission needs a polished 3-minute demo video, but the real app screen recording may be captured later.

### Decision

Create a HyperFrames-ready HTML composition in `demo_video/` based on `docs/video_script.md`. The app demo segment is represented by a Streamlit-style placeholder that can be replaced with real screen recording footage later.

### Consequences

- The video can be reviewed before the final screen recording exists
- The visual structure follows the existing narration script
- Real footage can be swapped into the 0:45-1:40 segment without rewriting the whole video
