"""
Yuval Itzhaki - Deep-Value Matching Dating App
Premium UI with Glassmorphism design system.
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Yuval Itzhaki | Deep-Value Dating",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from database.db import init_database
from auth.authenticator import init_session_state, login_user, register_user, logout, check_profile_exists
from pages.discovery import render_discovery_page
from pages.profile import render_profile_setup, render_profile_edit
from pages.matches import render_matches_page
from config.settings import APP_NAME, APP_TAGLINE
from seed_demo_data import seed_demo_data


def load_css():
    """Inject custom CSS design system."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_landing_page():
    st.markdown(f"""
    <div style="text-align:center; padding:40px 0 20px;">
        <h1 style="font-size:2.2rem; margin:0;">💜 {APP_NAME}</h1>
        <p style="color:rgba(250,249,246,0.6); font-size:16px; margin-top:8px;">{APP_TAGLINE}</p>
    </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div class="glass-card" style="margin-bottom:24px;">
        <div style="display:flex; justify-content:space-around; text-align:center;">
            <div style="flex:1;">
                <p style="font-size:28px; margin:0;">💡</p>
                <p style="font-size:12px; font-weight:600; margin:8px 0 2px;">Choose</p>
                <p style="font-size:11px; color:rgba(250,249,246,0.5); margin:0;">Your deep question</p>
            </div>
            <div style="flex:1;">
                <p style="font-size:28px; margin:0;">✍️</p>
                <p style="font-size:12px; font-weight:600; margin:8px 0 2px;">Engage</p>
                <p style="font-size:11px; color:rgba(250,249,246,0.5); margin:0;">Respond to unlock</p>
            </div>
            <div style="flex:1;">
                <p style="font-size:28px; margin:0;">💕</p>
                <p style="font-size:12px; font-weight:600; margin:8px 0 2px;">Connect</p>
                <p style="font-size:11px; color:rgba(250,249,246,0.5); margin:0;">Match on values</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(["Login", "Register"])

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
            new_username = st.text_input("Username *")
            new_email = st.text_input("Email *")
            new_password = st.text_input("Password *", type="password")
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
                        st.rerun()
                    else:
                        st.error(message)

    with st.expander("🧪 Demo Accounts"):
        st.markdown("""
        Password for all: **demo123**
        
        `noa_sunshine` · `maya_creative` · `shira_mindful` · `tamar_dreamer` · `lior_bold`
        """)


def render_sidebar():
    with st.sidebar:
        st.markdown(f"## 💜 {APP_NAME}")
        st.caption(f"@{st.session_state.username}")
        st.divider()

        if st.session_state.has_profile:
            page = st.radio("", ["✨ Discover", "💕 Matches", "👤 Profile"], label_visibility="collapsed")
        else:
            page = "👤 Profile"
            st.info("Complete your profile to start!")

        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    return page


def main():
    init_database()
    seed_demo_data()
    init_session_state()
    load_css()

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
        elif current_page == "👤 Profile":
            render_profile_edit()


if __name__ == "__main__":
    main()
