"""Matches Page - View matches, received insights, and chat."""

import streamlit as st
from database.db import get_matches_for_user, get_interactions_for_user, update_interaction_status, get_messages, send_message
from utils.helpers import format_time_ago


def render_matches_page():
    st.markdown("## 💕 Matches & Messages")

    user_id = st.session_state.user_id

    # Check if in active chat
    if 'active_chat' in st.session_state and st.session_state.active_chat:
        if st.button("← Back to Matches"):
            st.session_state.active_chat = None
            st.session_state.chat_other_profile = None
            st.rerun()
        else:
            render_chat(st.session_state.active_chat, user_id, st.session_state.get('chat_other_profile', {}))
        return

    tab1, tab2 = st.tabs(["💬 Matches", "📩 Received Insights"])

    with tab1:
        matches = get_matches_for_user(user_id)
        if not matches:
            st.info("💫 No matches yet. Keep engaging with profiles in Discovery!")
        else:
            st.markdown(f"You have **{len(matches)}** match{'es' if len(matches) != 1 else ''}!")
            for match in matches:
                other = match.get('other_profile', {})
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{other.get('display_name', 'Unknown')}, {other.get('age', '')}**")
                    last_msg = match.get('last_message')
                    if last_msg:
                        st.caption(f"💬 {last_msg['content'][:50]}")
                    else:
                        st.caption("No messages yet - say hi!")
                with col2:
                    if st.button("Chat", key=f"chat_{match['id']}"):
                        st.session_state.active_chat = match['id']
                        st.session_state.chat_other_profile = other
                        st.rerun()
                st.divider()

    with tab2:
        interactions = get_interactions_for_user(user_id)
        if not interactions:
            st.info("📭 No responses yet. When someone responds to your Insight Question, you'll see it here.")
        else:
            st.markdown(f"**{len(interactions)}** people responded to your insight question!")
            for interaction in interactions:
                st.markdown(f"**{interaction['display_name']}, {interaction['age']}**")
                st.markdown(f"*\"{interaction['insight_response']}\"*")
                st.caption(format_time_ago(interaction['created_at']))
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❤️ Like", key=f"like_{interaction['id']}"):
                        update_interaction_status(interaction['id'], 'liked')
                        st.success("Liked!")
                        st.rerun()
                with col2:
                    if st.button("👋 Pass", key=f"pass_{interaction['id']}"):
                        update_interaction_status(interaction['id'], 'passed')
                        st.rerun()
                st.divider()


def render_chat(match_id, current_user_id, other_profile):
    other_name = other_profile.get('display_name', 'Unknown')
    st.markdown(f"### 💬 Chat with {other_name}")

    messages = get_messages(match_id)

    if not messages:
        st.info("💌 No messages yet. Say hello!")
    else:
        for msg in messages:
            is_mine = msg['sender_id'] == current_user_id
            if is_mine:
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**{other_name}:** {msg['content']}")

    with st.form(key=f"chat_form_{match_id}", clear_on_submit=True):
        new_message = st.text_input("Type a message...", label_visibility="collapsed")
        if st.form_submit_button("Send 📤", use_container_width=True):
            if new_message and new_message.strip():
                send_message(match_id, current_user_id, new_message.strip())
                st.rerun()
