"""
Seed script - Creates 5 demo accounts for testing.
Run this once on app startup to populate the database with fake profiles.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_database, create_user, create_profile, get_user_by_username
from auth.authenticator import hash_password


DEMO_USERS = [
    {
        "username": "noa_sunshine",
        "email": "noa@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Noa",
            "age": 26,
            "gender": "Female",
            "looking_for": "Men",
            "city": "Tel Aviv",
            "bio": "Yoga teacher by day, amateur chef by night. I believe in deep conversations over coffee and spontaneous road trips. Looking for someone who values growth and isn't afraid to be vulnerable.",
            "photos": [],
            "insight_question": "What does a perfect Sunday look like for you?",
            "insight_category": "lifestyle"
        }
    },
    {
        "username": "daniel_adventures",
        "email": "daniel@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Daniel",
            "age": 29,
            "gender": "Male",
            "looking_for": "Women",
            "city": "Jerusalem",
            "bio": "Software engineer who moonlights as a jazz pianist. I love hiking in the Negev, reading philosophy, and cooking Italian food. Seeking meaningful connections, not just swipes.",
            "photos": [],
            "insight_question": "What principle would you never compromise on, even if it cost you everything?",
            "insight_category": "values"
        }
    },
    {
        "username": "maya_creative",
        "email": "maya@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Maya",
            "age": 24,
            "gender": "Female",
            "looking_for": "Everyone",
            "city": "Haifa",
            "bio": "Graphic designer and street art enthusiast. I collect vinyl records and make my own hot sauce. Life is too short for small talk - let's go deep from the start.",
            "photos": [],
            "insight_question": "What's a belief you held strongly that you've since changed your mind about?",
            "insight_category": "philosophy"
        }
    },
    {
        "username": "omer_explorer",
        "email": "omer@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Omer",
            "age": 31,
            "gender": "Male",
            "looking_for": "Women",
            "city": "Tel Aviv",
            "bio": "Marine biologist who's visited 40 countries. When I'm not diving, you'll find me at a local bookshop or trying to perfect my sourdough recipe. I value curiosity above all.",
            "photos": [],
            "insight_question": "If money wasn't an issue, how would you spend your days?",
            "insight_category": "dreams"
        }
    },
    {
        "username": "shira_mindful",
        "email": "shira@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Shira",
            "age": 27,
            "gender": "Female",
            "looking_for": "Men",
            "city": "Ramat Gan",
            "bio": "Clinical psychologist in training. I practice meditation, love board game nights, and am always down for a deep conversation about what makes us human. Authenticity is my love language.",
            "photos": [],
            "insight_question": "What is your biggest fear, and how do you face it?",
            "insight_category": "fears"
        }
    }
]


def seed_demo_data():
    """Create demo users and profiles if they don't exist."""
    init_database()
    created = 0
    
    for user_data in DEMO_USERS:
        # Check if user already exists
        if get_user_by_username(user_data["username"]):
            continue
        
        # Create user
        password_hash = hash_password(user_data["password"])
        user_id = create_user(user_data["username"], user_data["email"], password_hash)
        
        # Create profile
        p = user_data["profile"]
        create_profile(
            user_id=user_id,
            display_name=p["display_name"],
            age=p["age"],
            gender=p["gender"],
            looking_for=p["looking_for"],
            city=p["city"],
            bio=p["bio"],
            photos=p["photos"],
            insight_question=p["insight_question"],
            insight_category=p["insight_category"]
        )
        created += 1
    
    return created


if __name__ == "__main__":
    count = seed_demo_data()
    print(f"Created {count} demo accounts.")
    print("\nDemo accounts (all password: demo123):")
    for u in DEMO_USERS:
        print(f"  - {u['username']} ({u['profile']['display_name']}, {u['profile']['age']}, {u['profile']['city']})")
