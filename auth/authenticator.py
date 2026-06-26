"""Authentication module for Yuval Itzhaki Dating App."""

import bcrypt
import streamlit as st
from database.db import create_user, get_user_by_username, get_user_by_email, get_profile_by_user_id


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def register_user(username, email, password):
    if len(username) < 3:
        return False, "Username must be at least 3 characters.", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None
    if '@' not in email or '.' not in email:
        return False, "Please enter a valid email address.", None
    if get_user_by_username(username):
        return False, "Username already taken.", None
    if get_user_by_email(email):
        return False, "Email already registered.", None
    password_hash = hash_password(password)
    user_id = create_user(username, email, password_hash)
    return True, "Registration successful!", user_id


def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "Username not found.", None
    if not user['is_active']:
        return False, "Account is deactivated.", None
    if not verify_password(password, user['password_hash']):
        return False, "Incorrect password.", None
    return True, "Login successful!", user


def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'has_profile' not in st.session_state:
        st.session_state.has_profile = False


def logout():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.has_profile = False


def check_profile_exists(user_id):
    profile = get_profile_by_user_id(user_id)
    return profile is not None
