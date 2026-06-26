"""Matches Page - View matches and high-quality chat interface."""

import streamlit as st
from database.db import get_matches_for_user, get_messages, send_message
from utils.helpers import format_time_ago


def render_matches_page():
    user_id = st.session_state.user_id

    # Initialize chat state
    if 'active_chat' not in st.session_state:
        st.session_state.active_chat = None
    if 'chat_other_profile' not in st.session_state:
        st.session_state.chat_other_profile = None

    # If in active chat, show chat
    if st.session_state.active_chat:
        render_chat_interface(
            st.session_state.active_chat,
            user_id,
            st.session_state.chat_other_profile
        )
        return

    # Show matches list
    render_matches_list(user_id)


def render_matches_list(user_id):
    """Show list of all matches."""
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <h2 style="margin:0;">💕 Your Matches</h2>
        <p style="color:rgba(250,249,246,0.5); font-size:14px;">People you've connected with</p>
    </div>
    """, unsafe_allow_html=True)

    matches = get_matches_for_user(user_id)

    if not matches:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:50px 28px;">
            <p style="font-size:48px; margin:0;">💫</p>
            <h3 style="margin:16px 0 8px;">No matches yet</h3>
            <p style="color:rgba(250,249,246,0.5);">
                Keep engaging with profiles in Discovery!<br>
                When both of you respond to each other's insights, it's a match.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    for match in matches:
        other = match.get('other_profile', {})
        last_msg = match.get('last_message')
        
        # Get avatar
        photo_html = ""
        if other.get('photos') and len(other['photos']) > 0:
            photo_src = other['photos'][0]
            photo_html = f'<img src="{photo_src}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">'
        else:
            photo_html = '<div style="width:50px; height:50px; border-radius:50%; background:linear-gradient(135deg,#7c3aed,#a855f7); display:flex; align-items:center; justify-content:center; font-size:20px;">💜</div>'

        # Last message preview
        msg_preview = ""
        if last_msg:
            content = last_msg['content']
            if len(content) > 40:
                content = content[:40] + "..."
            msg_preview = f'<p style="margin:2px 0 0; font-size:13px; color:rgba(250,249,246,0.5);">{content}</p>'
        else:
            msg_preview = '<p style="margin:2px 0 0; font-size:13px; color:rgba(250,249,246,0.4);">Say hello! 👋</p>'

        st.markdown(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:12px; display:flex; align-items:center; gap:14px; cursor:pointer;">
            {photo_html}
            <div style="flex:1;">
                <p style="margin:0; font-weight:600; font-size:15px;">{other.get('display_name', 'Unknown')}, {other.get('age', '')}</p>
                {msg_preview}
            </div>
            <p style="margin:0; font-size:12px; color:rgba(250,249,246,0.3);">📍 {other.get('city', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"💬 Chat with {other.get('display_name', 'Unknown')}", key=f"open_chat_{match['id']}", use_container_width=True):
            st.session_state.active_chat = match['id']
            st.session_state.chat_other_profile = other
            st.rerun()


def render_chat_interface(match_id, current_user_id, other_profile):
    """High-quality chat interface."""
    other_name = other_profile.get('display_name', 'Unknown') if other_profile else 'Unknown'
    
    # Back button
    if st.button("← Back to Matches", key="back_to_matches"):
        st.session_state.active_chat = None
        st.session_state.chat_other_profile = None
        st.rerun()

    # Chat header
    photo_src = ""
    if other_profile and other_profile.get('photos') and len(other_profile['photos']) > 0:
        photo_src = other_profile['photos'][0]
        avatar_html = f'<img src="{photo_src}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">'
    else:
        avatar_html = '<div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg,#7c3aed,#a855f7); display:flex; align-items:center; justify-content:center;">💜</div>'

    st.markdown(f"""
    <div class="glass-card" style="padding:14px 20px; margin-bottom:16px; display:flex; align-items:center; gap:12px;">
        {avatar_html}
        <div>
            <p style="margin:0; font-weight:600; font-size:16px;">{other_name}</p>
            <p style="margin:0; font-size:12px; color:rgba(250,249,246,0.5);">Matched ✨</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Messages
    messages = get_messages(match_id)

    if not messages:
        st.markdown("""
        <div style="text-align:center; padding:40px; color:rgba(250,249,246,0.4);">
            <p style="font-size:32px;">💌</p>
            <p>Start the conversation!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Chat messages container
        st.markdown('<div style="max-height:400px; overflow-y:auto; padding:8px 0;">', unsafe_allow_html=True)
        
        for msg in messages:
            is_mine = msg['sender_id'] == current_user_id
            
            if is_mine:
                # My message - right aligned, violet
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin-bottom:10px;">
                    <div style="max-width:75%; padding:12px 16px; border-radius:18px 18px 4px 18px; 
                         background:linear-gradient(135deg, #7c3aed, #a855f7); color:white;">
                        <p style="margin:0; font-size:14px; line-height:1.5; color:white !important;">{msg['content']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Their message - left aligned, glass
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-start; margin-bottom:10px;">
                    <div style="max-width:75%; padding:12px 16px; border-radius:18px 18px 18px 4px; 
                         background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.1);">
                        <p style="margin:0; font-size:14px; line-height:1.5;">{msg['content']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Message input
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form(key=f"chat_send_{match_id}", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            new_message = st.text_input(
                "Message",
                placeholder="Type a message...",
                label_visibility="collapsed",
                key=f"msg_input_{match_id}"
            )
        with col2:
            sent = st.form_submit_button("📤", use_container_width=True)
        
        if sent and new_message and new_message.strip():
            send_message(match_id, current_user_id, new_message.strip())
            st.rerun()
