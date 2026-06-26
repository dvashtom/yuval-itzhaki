"""
Yuval Itzhaki - Deep-Value Matching Dating App
Main entry point for the Streamlit application.
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Yuval Itzhaki | Deep-Value Dating",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="expanded"
)

from database.db import init_database
from auth.authenticator import init_session_state, login_user, register_user, logout, check_profile_exists
from pages.discovery import render_discovery_page
from pages.profile import render_profile_setup, render_profile_edit
from pages.matches import render_matches_page
from config.settings import APP_NAME, APP_TAGLINE
from seed_demo_data import seed_demo_data


def render_landing_page():
    st.markdown(f"# 💜 {APP_NAME}")
    st.markdown(f"### *{APP_TAGLINE}*")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**💡 Choose Your Question**")
        st.caption("Pick a deep question that reveals character")
    with col2:
        st.markdown("**✍️ Engage First**")
        st.caption("Answer their question to unlock profiles")
    with col3:
        st.markdown("**💕 Match on Values**")
        st.caption("Connect based on who you really are")

    st.divider()

    login_tab, register_tab = st.tabs(["🔑 Login", "✨ Register"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
            if submitted:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    success, message, user_data = login_user(username.strip(), password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_data['id']
                        st.session_state.username = user_data['username']
                        st.session_state.has_profile = check_profile_exists(user_data['id'])
                        st.rerun()
                    else:
                        st.error(message)

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Username *", placeholder="Min 3 characters")
            new_email = st.text_input("Email *")
            new_password = st.text_input("Password *", type="password", placeholder="Min 6 characters")
            confirm_password = st.text_input("Confirm Password *", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            if submitted:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords don't match.")
                else:
                    success, message, user_id = register_user(new_username.strip(), new_email.strip().lower(), new_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = new_username.strip()
                        st.session_state.has_profile = False
                        st.success(message + " Now create your profile!")
                        st.rerun()
                    else:
                        st.error(message)

    with st.expander("🧪 Demo Accounts (for testing)"):
        st.markdown("""
        All demo accounts use password: **demo123**
        
        | Username | Name | Age | City |
        |----------|------|-----|------|
        | noa_sunshine | Noa | 26 | Tel Aviv |
        | maya_creative | Maya | 24 | Haifa |
        | shira_mindful | Shira | 27 | Ramat Gan |
        | tamar_dreamer | Tamar | 28 | Tel Aviv |
        | lior_bold | Lior | 25 | Jerusalem |
        """)


def render_sidebar():
    with st.sidebar:
        st.markdown(f"## 💜 {APP_NAME}")
        st.caption(f"Welcome, {st.session_state.username}!")
        st.divider()

        if st.session_state.has_profile:
            page = st.radio("Navigate", ["✨ Discover", "💕 Matches", "👤 My Profile"], label_visibility="collapsed")
        else:
            page = "👤 My Profile"
            st.info("Complete your profile to start!")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    return page


def main():
    init_database()
    seed_demo_data()
    init_session_state()

    if not st.session_state.authenticated:
        render_landing_page()
    else:
        current_page = render_sidebar()
        if not st.session_state.has_profile:
            render_profile_setup()
        elif current_page == "✨ Discover":
            render_discovery_page()
        elif current_page == "💕 Matches":
            render_matches_page()
        elif current_page == "👤 My Profile":
            render_profile_edit()


if __name__ == "__main__":
    main()
