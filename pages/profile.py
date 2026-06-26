"""Profile Page - Create and edit user profile with Insight Question."""

import streamlit as st
from database.db import create_profile, get_profile_by_user_id, update_profile
from utils.helpers import image_to_base64
from config.settings import (
    INSIGHT_CATEGORIES, PRESET_INSIGHT_QUESTIONS,
    GENDER_OPTIONS, LOOKING_FOR_OPTIONS, MAX_BIO_LENGTH, MAX_PHOTOS
)


def render_profile_setup():
    st.markdown("## 🌟 Create Your Profile")
    st.markdown("*Set up your profile with your unique Insight Question*")

    with st.form("profile_setup_form"):
        st.subheader("Basic Information")

        display_name = st.text_input("Display Name *", placeholder="Your name (required)")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age *", min_value=18, max_value=99, value=25)
            gender = st.selectbox("Gender *", GENDER_OPTIONS)
        with col2:
            looking_for = st.selectbox("Looking For *", LOOKING_FOR_OPTIONS)
            city = st.text_input("City", placeholder="Where are you based?")

        bio = st.text_area("Bio", max_chars=MAX_BIO_LENGTH, height=100,
                          placeholder="Tell people about yourself...")

        st.subheader("Photos")
        st.caption(f"Upload up to {MAX_PHOTOS} photos (optional)")
        uploaded_photos = []
        photo_cols = st.columns(MAX_PHOTOS)
        for i in range(MAX_PHOTOS):
            with photo_cols[i]:
                photo = st.file_uploader(f"Photo {i+1}", type=['jpg', 'jpeg', 'png'], key=f"photo_{i}")
                if photo:
                    uploaded_photos.append(photo)

        st.subheader("💡 Your Insight Question")
        st.info("This is what makes you stand out. Choose a deep question that potential matches must answer before they can see your full profile.")

        insight_category = st.selectbox(
            "Question Category *",
            options=list(INSIGHT_CATEGORIES.keys()),
            format_func=lambda x: INSIGHT_CATEGORIES[x]
        )

        question_type = st.radio("Choose your question", ["Pick from presets", "Write my own"], horizontal=True)

        insight_question = ""
        if question_type == "Pick from presets":
            presets = PRESET_INSIGHT_QUESTIONS.get(insight_category, [])
            if presets:
                insight_question = st.selectbox("Select a question", presets)
        else:
            insight_question = st.text_input("Write your own question *",
                                           placeholder="Ask something meaningful (at least 5 characters)...")

        submitted = st.form_submit_button("✨ Create Profile", use_container_width=True, type="primary")

        if submitted:
            if not display_name or not display_name.strip():
                st.error("⚠️ Please enter a display name at the top of the form.")
                return
            if not insight_question or len(insight_question.strip()) < 5:
                st.error("⚠️ Please select or write an Insight Question (at least 5 characters).")
                return

            photos_base64 = []
            for photo in uploaded_photos:
                b64 = image_to_base64(photo)
                if b64:
                    photos_base64.append(b64)

            try:
                create_profile(
                    user_id=st.session_state.user_id,
                    display_name=display_name.strip(),
                    age=age,
                    gender=gender,
                    looking_for=looking_for,
                    city=city.strip() if city else "",
                    bio=bio.strip() if bio else "",
                    photos=photos_base64,
                    insight_question=insight_question.strip(),
                    insight_category=insight_category
                )
                st.session_state.has_profile = True
                st.success("🎉 Profile created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating profile: {str(e)}")


def render_profile_edit():
    st.markdown("## 👤 My Profile")

    profile = get_profile_by_user_id(st.session_state.user_id)
    if not profile:
        render_profile_setup()
        return

    # Show profile photos
    photos = profile.get('photos', [])
    if photos and len(photos) > 0:
        st.subheader("Your Photos")
        photo_cols = st.columns(min(len(photos), 3))
        for i, photo_data in enumerate(photos):
            with photo_cols[i]:
                if photo_data.startswith("data:image/svg"):
                    st.markdown(f'<img src="{photo_data}" style="width:200px; height:200px; border-radius:12px; object-fit:cover;">', unsafe_allow_html=True)
                elif photo_data.startswith("data:image"):
                    st.markdown(f'<img src="{photo_data}" style="width:200px; height:200px; border-radius:12px; object-fit:cover;">', unsafe_allow_html=True)
                else:
                    st.image(photo_data, width=200)
        st.divider()

    st.markdown(f"### {profile['display_name']}, {profile['age']}")
    st.markdown(f"📍 {profile.get('city', 'No city set')}")
    st.markdown(f"**Bio:** {profile.get('bio', 'No bio yet.')}")

    category = INSIGHT_CATEGORIES.get(profile.get('insight_category', ''), 'Insight')
    st.markdown(f"**💡 Your Insight Question ({category}):**")
    st.markdown(f"*\"{profile['insight_question']}\"*")

    with st.expander("✏️ Edit Profile"):
        with st.form("edit_profile_form"):
            new_bio = st.text_area("Bio", value=profile.get('bio', ''), max_chars=MAX_BIO_LENGTH)
            new_city = st.text_input("City", value=profile.get('city', ''))
            new_looking_for = st.selectbox("Looking For", LOOKING_FOR_OPTIONS,
                index=LOOKING_FOR_OPTIONS.index(profile['looking_for']) if profile['looking_for'] in LOOKING_FOR_OPTIONS else 0)

            if st.form_submit_button("Save Changes", use_container_width=True):
                update_profile(st.session_state.user_id, bio=new_bio.strip(), city=new_city.strip(), looking_for=new_looking_for)
                st.success("Profile updated!")
                st.rerun()
