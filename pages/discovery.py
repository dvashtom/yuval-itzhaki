"""Discovery Feed Page - Premium glassmorphism card with Insight Layer."""

import streamlit as st
from utils.matching import get_discovery_feed
from database.db import create_interaction
from config.settings import INSIGHT_CATEGORIES


def render_discovery_page():
    user_id = st.session_state.user_id

    if 'discovery_feed' not in st.session_state:
        st.session_state.discovery_feed = get_discovery_feed(user_id)
    if 'discovery_index' not in st.session_state:
        st.session_state.discovery_index = 0
    if 'unlocked_profiles' not in st.session_state:
        st.session_state.unlocked_profiles = {}

    feed = st.session_state.discovery_feed
    index = st.session_state.discovery_index

    if not feed or index >= len(feed):
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:60px 28px;">
            <p style="font-size:48px; margin:0;">✨</p>
            <h3 style="margin:16px 0 8px;">You've seen everyone</h3>
            <p style="color:rgba(250,249,246,0.6);">Check back later for new profiles</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Refresh Feed"):
            st.session_state.discovery_feed = get_discovery_feed(user_id)
            st.session_state.discovery_index = 0
            st.rerun()
        return

    profile = feed[index]
    profile_user_id = profile['user_id']
    is_unlocked = profile_user_id in st.session_state.unlocked_profiles

    # Get photo URL
    photo_src = ""
    if profile.get('photos') and len(profile['photos']) > 0:
        photo_src = profile['photos'][0]

    category = INSIGHT_CATEGORIES.get(profile.get('insight_category', ''), 'Insight')
    locked_class = "" if is_unlocked else "locked"

    # Render the Discovery Card with glassmorphism
    st.markdown(f"""
    <div class="discovery-card">
        <div class="photo-container {locked_class}">
            <img src="{photo_src}" alt="{profile['display_name']}">
            <div class="photo-overlay">
                <h3 style="margin:0; font-size:22px; color:white;">{profile['display_name']}, {profile['age']}</h3>
                <p style="margin:4px 0 0; font-size:14px; color:rgba(255,255,255,0.7);">📍 {profile.get('city', 'Unknown')}</p>
            </div>
        </div>
        <div class="insight-section">
            <p class="insight-category">💡 {category}</p>
            <p class="insight-question">"{profile['insight_question']}"</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if is_unlocked:
        # Show unlocked content with reveal animation
        response = st.session_state.unlocked_profiles[profile_user_id]
        st.markdown(f"""
        <div class="glass-card profile-reveal" style="margin-top:16px;">
            <p style="color:#10b981; font-size:13px; font-weight:600; text-transform:uppercase; letter-spacing:1px;">🔓 Profile Unlocked</p>
            <p style="color:var(--text-primary); line-height:1.6; margin:12px 0;">{profile.get('bio', 'No bio yet.')}</p>
            <div style="background:rgba(124,58,237,0.1); border-radius:12px; padding:14px; margin-top:12px;">
                <p style="font-size:12px; color:#c9a96e; margin:0 0 6px;">Your response:</p>
                <p style="margin:0; color:var(--text-primary); font-style:italic;">"{response}"</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("➡️ Next Profile", type="primary"):
            st.session_state.discovery_index += 1
            st.rerun()
    else:
        # Locked - show response form
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form(key=f"insight_form_{index}"):
            response = st.text_area(
                "Your response to their question:",
                max_chars=300,
                height=100,
                placeholder="Write something genuine and thoughtful..."
            )
            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button("🔓 Unlock Profile", type="primary", use_container_width=True)
            with col2:
                skipped = st.form_submit_button("Skip", use_container_width=True)

            if submitted:
                if response and len(response.strip()) >= 10:
                    create_interaction(user_id, profile_user_id, response.strip())
                    st.session_state.unlocked_profiles[profile_user_id] = response.strip()
                    st.rerun()
                else:
                    st.error("Write at least 10 characters.")
            if skipped:
                st.session_state.discovery_index += 1
                st.rerun()

    # Progress
    st.markdown(f"""
    <p style="text-align:center; color:rgba(250,249,246,0.3); font-size:12px; margin-top:20px;">
        {index + 1} / {len(feed)}
    </p>
    """, unsafe_allow_html=True)
