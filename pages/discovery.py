"""Discovery Feed Page - The core experience with the Insight Layer."""

import streamlit as st
from utils.matching import get_discovery_feed
from database.db import create_interaction
from config.settings import INSIGHT_CATEGORIES


def show_photo(photos):
    """Display profile photo from base64 data."""
    if photos and len(photos) > 0:
        photo = photos[0]
        if photo.startswith("data:image"):
            st.markdown(f'<img src="{photo}" style="width:300px; height:300px; border-radius:16px; object-fit:cover; display:block; margin:0 auto;">', unsafe_allow_html=True)
        else:
            st.image(photo, width=300)
    else:
        st.markdown('<div style="width:300px; height:300px; background:linear-gradient(135deg,#667eea,#764ba2); border-radius:16px; display:flex; align-items:center; justify-content:center; margin:0 auto;"><span style="font-size:80px;">👤</span></div>', unsafe_allow_html=True)


def render_discovery_page():
    st.markdown("## ✨ Discover")
    st.markdown("*Connect through meaningful insights*")

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
        st.info("🌟 You've seen everyone! Check back later for new profiles.")
        if st.button("🔄 Refresh Feed"):
            st.session_state.discovery_feed = get_discovery_feed(user_id)
            st.session_state.discovery_index = 0
            st.rerun()
        return

    profile = feed[index]
    profile_user_id = profile['user_id']
    is_unlocked = profile_user_id in st.session_state.unlocked_profiles

    st.divider()

    # Show photo
    show_photo(profile.get('photos', []))

    st.markdown(f"### {profile['display_name']}, {profile['age']}")
    st.markdown(f"📍 {profile.get('city', 'Unknown location')}")

    if is_unlocked:
        # UNLOCKED - show full profile
        st.success("🔓 Profile unlocked!")
        st.markdown(f"**About:** {profile.get('bio', 'No bio yet.')}")

        response = st.session_state.unlocked_profiles[profile_user_id]
        category = INSIGHT_CATEGORIES.get(profile.get('insight_category', ''), 'Insight')
        st.markdown(f"**💡 {category}:** *\"{profile['insight_question']}\"*")
        st.markdown(f"**Your response:** {response}")

        if st.button("➡️ Next Profile", type="primary"):
            st.session_state.discovery_index += 1
            st.rerun()
    else:
        # LOCKED - show insight question gate
        category = INSIGHT_CATEGORIES.get(profile.get('insight_category', ''), 'Insight')
        st.markdown("---")
        st.markdown(f"**💡 {category}**")
        st.markdown(f"*\"{profile['insight_question']}\"*")
        st.caption("🔒 Respond to their question to unlock the full profile")

        with st.form(key=f"insight_form_{index}"):
            response = st.text_area(
                "Your thoughtful response:",
                max_chars=300,
                height=100,
                placeholder="Write a genuine, thoughtful response (min 10 characters)..."
            )
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("🔓 Submit & Unlock", type="primary", use_container_width=True)
            with col2:
                skipped = st.form_submit_button("⏭️ Skip", use_container_width=True)

            if submitted:
                if response and len(response.strip()) >= 10:
                    create_interaction(user_id, profile_user_id, response.strip())
                    st.session_state.unlocked_profiles[profile_user_id] = response.strip()
                    st.rerun()
                else:
                    st.error("Please write at least 10 characters.")
            if skipped:
                st.session_state.discovery_index += 1
                st.rerun()

    st.caption(f"Profile {index + 1} of {len(feed)}")
