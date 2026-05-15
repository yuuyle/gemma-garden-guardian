# HANDOFF.md

## Background

We are participating in Kaggle's "The Gemma 4 Good Hackathon".

The user wants to build a project quickly and submit it successfully. The main challenge is not only coding but also preparing a convincing demo, video, writeup, and public repository.

## Chosen idea

Project:

**Gemma Garden Guardian**

Description:

A photo-based AI field assistant for small-scale growers and home gardeners.

The app helps users understand visible crop or garden conditions from photos and produces safe, practical next actions.

## Why this idea

The user has prior interest in:

- home gardening
- crop monitoring
- computer vision
- IoT
- Raspberry Pi / ESP32
- AI assistants
- practical hackathon projects

This idea fits the hackathon because it has:

- social impact
- clear user story
- multimodal use of Gemma 4
- practical demo potential
- low hardware requirements
- good fit for Google Cloud usage

## Target users

- home gardeners
- small-scale farmers
- community garden users
- beginners
- elderly growers
- people in areas with limited expert access

## Impact framing

Main impact categories:

- Global Resilience
- Digital Equity
- Food security
- Small-scale agriculture support

Core message:

AI should not replace farmers or experts. It should help people observe earlier, act more safely, and learn from their own garden history.

## Technical direction

Use Google Cloud instead of local LLM inference.

The user's PC is not powerful enough to run Gemma 4 locally.

Preferred model:

```text
gemma-4-26b-a4b-it-maas
```

Key Gemma 4 features to show:

- image understanding
- text + image input
- structured JSON output
- function-calling-style tool workflow
- crop history context
- safe uncertainty-aware recommendations

## MVP workflow

1. User opens Streamlit app.
2. User uploads crop/garden image.
3. User enters crop type and notes.
4. App sends image and context to Gemma 4.
5. Gemma returns structured JSON.
6. App validates JSON.
7. App displays:
   - summary
   - observations
   - risk level
   - recommended actions
   - uncertainty
   - next photo suggestions
8. App saves result to observation log.
9. App creates todos from recommended actions.
10. Optional: app compares with previous observation.

## JSON output shape

The Gemma response should follow this shape:

```json
{
  "crop_type": "tomato",
  "overall_status": "needs_attention",
  "summary": "Short human-readable summary.",
  "observations": [
    {
      "category": "leaf",
      "finding": "Visible observation from image.",
      "confidence": "low|medium|high"
    }
  ],
  "risk_level": "low|medium|high",
  "risks": [
    {
      "name": "water_stress",
      "reason": "Why this may be a risk.",
      "confidence": "low|medium|high"
    }
  ],
  "recommended_actions": [
    {
      "priority": "high|medium|low",
      "action": "Practical next action.",
      "reason": "Why this action is suggested."
    }
  ],
  "uncertainty": [
    "What cannot be determined from the image."
  ],
  "next_photo_suggestions": [
    "What photo the user should take next."
  ]
}
```

## Important safety policy for the app

The app must not claim to diagnose plant diseases definitively.

Use uncertainty-aware wording.

Avoid specific pesticide recommendations.

Recommend human confirmation for high-risk decisions.

## Hackathon priorities

Priority order:

1. Working app
2. Clear Gemma 4 usage
3. Good README
4. Good video story
5. Kaggle writeup
6. Live demo
7. Optional technical extras

Fine-tuning is optional and should not block the MVP.

Local inference is optional and should not be attempted unless everything else is finished.

## Immediate next tasks

1. Create Streamlit mock UI.
2. Define JSON schema.
3. Implement mock response.
4. Implement Gemma client.
5. Add logging.
6. Add todo generation.
7. Prepare sample images.
8. Draft README.
9. Draft video script.
10. Draft Kaggle writeup.
