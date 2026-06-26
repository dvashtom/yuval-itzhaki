"""Insight prompt component - the core gate mechanism."""

import streamlit as st


def render_insight_form(profile, form_key):
    """Render the insight response form. Returns response text or None."""
    with st.form(key=form_key):
        response = st.text_area(
            "Your thoughtful response:",
            max_chars=300,
            height=100,
            placeholder="Write a genuine response (min 10 characters)..."
        )
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🔓 Submit & Unlock", type="primary", use_container_width=True)
        with col2:
            skipped = st.form_submit_button("⏭️ Skip", use_container_width=True)

        if submitted and response and len(response.strip()) >= 10:
            return response.strip()
        elif submitted:
            st.error("Please write at least 10 characters.")
        if skipped:
            return "SKIP"
    return None
