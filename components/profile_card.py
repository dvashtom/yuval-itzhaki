"""Reusable profile card component."""

import streamlit as st
from config.settings import INSIGHT_CATEGORIES


def render_locked_card(profile):
    """Render a profile card in LOCKED state - photo + insight question only."""
    if profile.get('photos') and len(profile['photos']) > 0:
        st.image(profile['photos'][0], width=300)
    st.markdown(f"### {profile['display_name']}, {profile['age']}")
    st.markdown(f"📍 {profile.get('city', 'Unknown')}")
    category = INSIGHT_CATEGORIES.get(profile.get('insight_category', ''), 'Insight')
    st.markdown(f"**💡 {category}**")
    st.markdown(f"*\"{profile['insight_question']}\"*")
    st.caption("🔒 Respond to unlock full profile")


def render_unlocked_card(profile):
    """Render a profile card in UNLOCKED state - full details."""
    if profile.get('photos') and len(profile['photos']) > 0:
        st.image(profile['photos'][0], width=300)
    st.markdown(f"### {profile['display_name']}, {profile['age']}")
    st.markdown(f"📍 {profile.get('city', 'Unknown')}")
    st.markdown(f"**About:** {profile.get('bio', 'No bio yet.')}")
    st.success("🔓 Profile unlocked!")
