"""Chat widget component for matched users."""

import streamlit as st
from database.db import get_messages, send_message


def render_chat(match_id, current_user_id, other_name):
    """Render chat interface for a match."""
    messages = get_messages(match_id)

    if not messages:
        st.info("💌 No messages yet. Say hello!")
    else:
        for msg in messages:
            is_mine = msg['sender_id'] == current_user_id
            prefix = "**You:**" if is_mine else f"**{other_name}:**"
            st.markdown(f"{prefix} {msg['content']}")

    with st.form(key=f"chat_{match_id}", clear_on_submit=True):
        new_msg = st.text_input("Message...", label_visibility="collapsed")
        if st.form_submit_button("Send 📤", use_container_width=True):
            if new_msg and new_msg.strip():
                send_message(match_id, current_user_id, new_msg.strip())
                st.rerun()
