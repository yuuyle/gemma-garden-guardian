from __future__ import annotations

import json
from typing import Any

import streamlit as st
from jsonschema import ValidationError
from dotenv import load_dotenv

from src.gemma_client import GemmaClient
from src.report import generate_weekly_report
from src.schemas import validate_analysis
from src.storage import DEFAULT_LOG_PATH, load_observations, log_observation
from src.tools import (
    build_observation_entry,
    calculate_risk_score,
    compare_with_previous,
    create_todo_items,
)


RISK_COLORS = {
    "low": "green",
    "medium": "orange",
    "high": "red",
}


def render_status_badge(label: str, value: str) -> None:
    color = RISK_COLORS.get(value.lower(), "blue")
    st.markdown(f"**{label}:** :{color}[{value.replace('_', ' ').title()}]")


def render_dashboard(
    analysis: dict[str, Any],
    todos: list[dict[str, Any]],
    risk_score: int,
    comparison: list[str],
) -> None:
    st.subheader("Observation Dashboard")

    metric_cols = st.columns(3)
    metric_cols[0].metric("Crop", analysis["crop_type"].title())
    metric_cols[1].metric("Status", analysis["overall_status"].replace("_", " ").title())
    metric_cols[2].metric("Risk Score", f"{risk_score}/100", analysis["risk_level"].title())

    st.info(analysis["summary"])

    left, right = st.columns([1, 1])

    with left:
        st.markdown("### Visible observations")
        for item in analysis["observations"]:
            st.markdown(
                f"- **{item['category'].title()}**: {item['finding']} "
                f"_{item['confidence']} confidence_"
            )

        st.markdown("### Possible risks")
        render_status_badge("Overall risk", analysis["risk_level"])
        for risk in analysis["risks"]:
            st.markdown(
                f"- **{risk['name'].replace('_', ' ').title()}**: {risk['reason']} "
                f"_{risk['confidence']} confidence_"
            )

    with right:
        st.markdown("### Recommended action todos")
        for todo in todos:
            priority = todo["priority"].title()
            st.checkbox(
                f"{priority}: {todo['title']}",
                value=False,
                help=todo["reason"],
            )

        st.markdown("### Uncertainty")
        for item in analysis["uncertainty"]:
            st.markdown(f"- {item}")

        st.markdown("### Next photos to capture")
        for item in analysis["next_photo_suggestions"]:
            st.markdown(f"- {item}")

    st.markdown("### Previous Observation Comparison")
    for item in comparison:
        st.markdown(f"- {item}")

    with st.expander("Structured JSON"):
        st.json(analysis)


def render_history_panel(history: list[dict[str, Any]]) -> None:
    st.subheader("Observation History")
    if not history:
        st.write("No saved observations yet.")
        return

    for entry in history[:5]:
        analysis = entry.get("analysis", {})
        label = (
            f"{entry.get('created_at', 'unknown time')} | "
            f"{analysis.get('crop_type', 'unknown crop')} | "
            f"{analysis.get('risk_level', 'unknown')} risk"
        )
        with st.expander(label):
            st.write(analysis.get("summary", "No summary saved."))
            st.caption(f"Image: {entry.get('image_name', 'unknown')} | Source: {entry.get('source', 'unknown')}")
            st.json(entry)


def main() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="Gemma Garden Guardian",
        layout="wide",
    )

    st.title("Gemma Garden Guardian")
    st.caption("A cautious AI field assistant for small-scale growers powered by Gemma 4.")

    st.warning(
        "This demo is not a plant disease diagnosis tool. It highlights visible signs, "
        "possible risks, uncertainty, and safe next actions to confirm locally."
    )

    client = GemmaClient()
    history = load_observations(limit=10)

    with st.sidebar:
        st.header("Analysis Setup")
        st.write(f"Current mode: **{client.config.mode}**")
        st.caption("Use GEMMA_GARDEN_MODE=mock for local development without Google Cloud credentials.")
        st.caption(f"Log path: `{DEFAULT_LOG_PATH}`")
        st.divider()
        render_history_panel(history)
        st.divider()
        with st.expander("Weekly report"):
            st.markdown(generate_weekly_report(history))

    input_col, preview_col = st.columns([1, 1])

    with input_col:
        uploaded_image = st.file_uploader(
            "Upload a crop or garden photo",
            type=["jpg", "jpeg", "png", "webp", "svg"],
        )
        crop_type = st.text_input("Crop type", placeholder="e.g. tomato, basil, cucumber")
        notes = st.text_area(
            "Notes",
            placeholder="Describe recent weather, watering, visible changes, or concerns.",
            height=140,
        )
        analyze = st.button("Analyze crop photo", type="primary")

    with preview_col:
        st.subheader("Photo Preview")
        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)
        else:
            st.write("Upload an image to preview it here.")

    if analyze:
        if not uploaded_image:
            st.error("Please upload an image before running the mock analysis.")
            return

        result = client.analyze_image(
            image_bytes=uploaded_image.getvalue(),
            crop_type=crop_type.strip() or "unknown crop",
            notes=notes.strip(),
            image_name=uploaded_image.name,
        )
        analysis = result.analysis

        try:
            validate_analysis(analysis)
        except ValidationError as exc:
            st.error(f"Analysis response failed schema validation: {exc.message}")
            st.code(json.dumps(analysis, indent=2), language="json")
            return

        todos = create_todo_items(analysis)
        risk_score = calculate_risk_score(analysis)
        comparison = compare_with_previous(analysis, history[0] if history else None)
        entry = build_observation_entry(
            analysis=analysis,
            image_name=uploaded_image.name,
            notes=notes.strip(),
            source=result.source,
            risk_score=risk_score,
        )
        saved_path = log_observation(entry)

        if result.used_fallback:
            st.warning(f"Using fallback analysis because the Gemma client returned an error: {result.error}")
        st.success(f"Observation saved to {saved_path}")
        render_dashboard(analysis, todos=todos, risk_score=risk_score, comparison=comparison)


if __name__ == "__main__":
    main()
