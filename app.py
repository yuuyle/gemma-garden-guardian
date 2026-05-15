from __future__ import annotations

import json
from typing import Any

import streamlit as st
from jsonschema import ValidationError

from src.gemma_client import analyze_image_mock
from src.schemas import validate_analysis


RISK_COLORS = {
    "low": "green",
    "medium": "orange",
    "high": "red",
}


def render_status_badge(label: str, value: str) -> None:
    color = RISK_COLORS.get(value.lower(), "blue")
    st.markdown(f"**{label}:** :{color}[{value.replace('_', ' ').title()}]")


def render_dashboard(analysis: dict[str, Any]) -> None:
    st.subheader("Observation Dashboard")

    metric_cols = st.columns(3)
    metric_cols[0].metric("Crop", analysis["crop_type"].title())
    metric_cols[1].metric("Status", analysis["overall_status"].replace("_", " ").title())
    metric_cols[2].metric("Risk", analysis["risk_level"].title())

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
        for action in analysis["recommended_actions"]:
            priority = action["priority"].title()
            st.checkbox(
                f"{priority}: {action['action']}",
                value=False,
                help=action["reason"],
            )

        st.markdown("### Uncertainty")
        for item in analysis["uncertainty"]:
            st.markdown(f"- {item}")

        st.markdown("### Next photos to capture")
        for item in analysis["next_photo_suggestions"]:
            st.markdown(f"- {item}")

    with st.expander("Structured JSON"):
        st.json(analysis)


def main() -> None:
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

    with st.sidebar:
        st.header("Analysis Setup")
        st.write("Current mode: **mock**")
        st.caption("Google Cloud credentials are not required for Phase 1 and Phase 2.")

    input_col, preview_col = st.columns([1, 1])

    with input_col:
        uploaded_image = st.file_uploader(
            "Upload a crop or garden photo",
            type=["jpg", "jpeg", "png", "webp"],
        )
        crop_type = st.text_input("Crop type", placeholder="e.g. tomato, basil, cucumber")
        notes = st.text_area(
            "Notes",
            placeholder="Describe recent weather, watering, visible changes, or concerns.",
            height=140,
        )
        analyze = st.button("Analyze with mock Gemma response", type="primary")

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

        analysis = analyze_image_mock(
            crop_type=crop_type.strip() or "unknown crop",
            notes=notes.strip(),
            image_name=uploaded_image.name,
        )

        try:
            validate_analysis(analysis)
        except ValidationError as exc:
            st.error(f"Mock response failed schema validation: {exc.message}")
            st.code(json.dumps(analysis, indent=2), language="json")
            return

        render_dashboard(analysis)


if __name__ == "__main__":
    main()
