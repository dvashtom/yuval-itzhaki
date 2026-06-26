"""
Seed script - Creates 5 demo accounts for testing.
All demo users are female with generated avatar images.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_database, create_user, create_profile, get_user_by_username
from auth.authenticator import hash_password


# Generate simple SVG avatars as base64 for demo users
def generate_avatar(name, color):
    """Generate a simple colored avatar with initials as base64 SVG."""
    initial = name[0].upper()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
        <rect width="400" height="400" fill="{color}" rx="20"/>
        <text x="200" y="260" font-family="Arial" font-size="180" fill="white" text-anchor="middle">{initial}</text>
        <text x="200" y="340" font-family="Arial" font-size="40" fill="rgba(255,255,255,0.8)" text-anchor="middle">{name}</text>
    </svg>'''
    import base64
    encoded = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{encoded}"


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
            "color": "#E91E63",
            "insight_question": "What does a perfect Sunday look like for you?",
            "insight_category": "lifestyle"
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
            "looking_for": "Men",
            "city": "Haifa",
            "bio": "Graphic designer and street art enthusiast. I collect vinyl records and make my own hot sauce. Life is too short for small talk - let's go deep from the start.",
            "color": "#9C27B0",
            "insight_question": "What's a belief you held strongly that you've since changed your mind about?",
            "insight_category": "philosophy"
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
            "color": "#FF5722",
            "insight_question": "What is your biggest fear, and how do you face it?",
            "insight_category": "fears"
        }
    },
    {
        "username": "tamar_dreamer",
        "email": "tamar@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Tamar",
            "age": 28,
            "gender": "Female",
            "looking_for": "Men",
            "city": "Tel Aviv",
            "bio": "Marine biologist who's visited 30 countries. When I'm not diving, you'll find me at a local bookshop or trying to perfect my sourdough recipe. I value curiosity above all.",
            "color": "#00BCD4",
            "insight_question": "If money wasn't an issue, how would you spend your days?",
            "insight_category": "dreams"
        }
    },
    {
        "username": "lior_bold",
        "email": "lior@demo.com",
        "password": "demo123",
        "profile": {
            "display_name": "Lior",
            "age": 25,
            "gender": "Female",
            "looking_for": "Men",
            "city": "Jerusalem",
            "bio": "Music producer and jazz singer. I love hiking, reading philosophy, and cooking for friends. Seeking meaningful connections built on honesty and shared values.",
            "color": "#673AB7",
            "insight_question": "What principle would you never compromise on, even if it cost you everything?",
            "insight_category": "values"
        }
    }
]


def seed_demo_data():
    """Create demo users and profiles if they don't exist."""
    init_database()
    created = 0
    
    for user_data in DEMO_USERS:
        if get_user_by_username(user_data["username"]):
            continue
        
        password_hash = hash_password(user_data["password"])
        user_id = create_user(user_data["username"], user_data["email"], password_hash)
        
        p = user_data["profile"]
        avatar = generate_avatar(p["display_name"], p["color"])
        
        create_profile(
            user_id=user_id,
            display_name=p["display_name"],
            age=p["age"],
            gender=p["gender"],
            looking_for=p["looking_for"],
            city=p["city"],
            bio=p["bio"],
            photos=[avatar],
            insight_question=p["insight_question"],
            insight_category=p["insight_category"]
        )
        created += 1
    
    return created


if __name__ == "__main__":
    count = seed_demo_data()
    print(f"Created {count} demo accounts.")
