"""
Seed script - Creates 25 demo accounts + 1 match for user 'dvash'.
All demo users are female with generated avatar images.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import (
    init_database, create_user, create_profile, get_user_by_username,
    create_interaction, get_profile_by_user_id, send_message
)
from auth.authenticator import hash_password
import base64


def generate_avatar(name, color):
    """Generate a simple colored avatar with initials as base64 SVG."""
    initial = name[0].upper()
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400"><rect width="400" height="400" fill="{color}" rx="20"/><text x="200" y="260" font-family="Arial" font-size="180" fill="white" text-anchor="middle">{initial}</text><text x="200" y="340" font-family="Arial" font-size="40" fill="rgba(255,255,255,0.8)" text-anchor="middle">{name}</text></svg>'
    encoded = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{encoded}"


DEMO_USERS = [
    {"username": "noa_sunshine", "email": "noa@demo.com", "name": "Noa", "age": 26, "city": "Tel Aviv", "color": "#E91E63", "bio": "Yoga teacher by day, amateur chef by night. Deep conversations over coffee and spontaneous road trips.", "question": "What does a perfect Sunday look like for you?", "category": "lifestyle"},
    {"username": "maya_creative", "email": "maya@demo.com", "name": "Maya", "age": 24, "city": "Haifa", "color": "#9C27B0", "bio": "Graphic designer and street art enthusiast. Vinyl records collector. Life is too short for small talk.", "question": "What belief have you changed your mind about?", "category": "philosophy"},
    {"username": "shira_mindful", "email": "shira@demo.com", "name": "Shira", "age": 27, "city": "Ramat Gan", "color": "#FF5722", "bio": "Clinical psychologist in training. Meditation, board games, and deep conversations about what makes us human.", "question": "What is your biggest fear, and how do you face it?", "category": "fears"},
    {"username": "tamar_dreamer", "email": "tamar@demo.com", "name": "Tamar", "age": 28, "city": "Tel Aviv", "color": "#00BCD4", "bio": "Marine biologist, 30 countries visited. Bookshops, sourdough, and endless curiosity.", "question": "If money wasn't an issue, how would you spend your days?", "category": "dreams"},
    {"username": "lior_bold", "email": "lior@demo.com", "name": "Lior", "age": 25, "city": "Jerusalem", "color": "#673AB7", "bio": "Music producer and jazz singer. Hiking, philosophy, cooking for friends.", "question": "What principle would you never compromise on?", "category": "values"},
    {"username": "dana_wanderer", "email": "dana@demo.com", "name": "Dana", "age": 29, "city": "Tel Aviv", "color": "#3F51B5", "bio": "Travel photographer chasing golden hours. Coffee addict. Believes in karma and kind strangers.", "question": "What's the most meaningful trip you've ever taken?", "category": "dreams"},
    {"username": "yael_serene", "email": "yael@demo.com", "name": "Yael", "age": 26, "city": "Herzliya", "color": "#009688", "bio": "Architect who designs tiny homes. Minimalist living, ocean swimming, poetry at midnight.", "question": "What does home mean to you?", "category": "values"},
    {"username": "rotem_spark", "email": "rotem@demo.com", "name": "Rotem", "age": 23, "city": "Beer Sheva", "color": "#FF9800", "bio": "Medical student and amateur stand-up comedian. Laughter is my love language.", "question": "What makes you laugh until you cry?", "category": "lifestyle"},
    {"username": "hila_rhythm", "email": "hila@demo.com", "name": "Hila", "age": 30, "city": "Tel Aviv", "color": "#795548", "bio": "Dance instructor. Movement is my meditation. Seeking someone who moves through life with intention.", "question": "How do you express love without words?", "category": "values"},
    {"username": "michal_wise", "email": "michal@demo.com", "name": "Michal", "age": 27, "city": "Raanana", "color": "#607D8B", "bio": "Data scientist by day, fantasy novelist by night. Two cats named after philosophers.", "question": "What book changed how you see the world?", "category": "philosophy"},
    {"username": "sapir_glow", "email": "sapir@demo.com", "name": "Sapir", "age": 24, "city": "Netanya", "color": "#E040FB", "bio": "Jewelry designer working with recycled metals. Sustainability is a lifestyle, not a trend.", "question": "What small daily act makes you feel most alive?", "category": "lifestyle"},
    {"username": "ori_flame", "email": "ori@demo.com", "name": "Ori", "age": 28, "city": "Tel Aviv", "color": "#FF6D00", "bio": "Startup founder in edtech. Running marathons and reading biographies. Driven but never too busy for people.", "question": "What failure taught you the most?", "category": "fears"},
    {"username": "neta_bloom", "email": "neta@demo.com", "name": "Neta", "age": 25, "city": "Haifa", "color": "#4CAF50", "bio": "Botanical garden curator. Growing things is my superpower. Gentle soul with wild dreams.", "question": "What would you grow if you had infinite patience?", "category": "dreams"},
    {"username": "inbar_sky", "email": "inbar@demo.com", "name": "Inbar", "age": 26, "city": "Eilat", "color": "#2196F3", "bio": "Diving instructor and marine conservation activist. Salt in my hair, purpose in my heart.", "question": "What's worth protecting at all costs?", "category": "values"},
    {"username": "talia_moon", "email": "talia@demo.com", "name": "Talia", "age": 31, "city": "Jerusalem", "color": "#311B92", "bio": "Classical pianist turned electronic music producer. Contradictions make life interesting.", "question": "What two parts of yourself seem contradictory but coexist?", "category": "philosophy"},
    {"username": "gal_wonder", "email": "gal@demo.com", "name": "Gal", "age": 27, "city": "Tel Aviv", "color": "#C2185B", "bio": "UX researcher obsessed with human behavior. Film festivals, vintage shops, late-night conversations.", "question": "What's something you pretend to understand but don't?", "category": "fears"},
    {"username": "amit_gentle", "email": "amit@demo.com", "name": "Amit", "age": 29, "city": "Rehovot", "color": "#00695C", "bio": "Veterinarian with a weakness for rescued animals. Cooking therapy, nature walks, genuine people.", "question": "What does kindness look like in everyday life?", "category": "values"},
    {"username": "keren_light", "email": "keren@demo.com", "name": "Keren", "age": 24, "city": "Givatayim", "color": "#F57C00", "bio": "Illustrator and children's book author. Colorful mind, quiet soul. Tea over coffee, always.", "question": "What story do you keep telling yourself?", "category": "philosophy"},
    {"username": "lihi_breeze", "email": "lihi@demo.com", "name": "Lihi", "age": 26, "city": "Kfar Saba", "color": "#1565C0", "bio": "Environmental lawyer fighting for clean oceans. Surfing, pottery, and belief in systemic change.", "question": "What would you fight for even if you might lose?", "category": "values"},
    {"username": "shahar_dawn", "email": "shahar@demo.com", "name": "Shahar", "age": 28, "city": "Tel Aviv", "color": "#AD1457", "bio": "Chef at a farm-to-table restaurant. Food is love made visible. Early mornings, farmers markets, gratitude.", "question": "What's your earliest happy memory?", "category": "lifestyle"},
    {"username": "eden_peace", "email": "eden@demo.com", "name": "Eden", "age": 25, "city": "Modiin", "color": "#6A1B9A", "bio": "Conflict resolution mediator. I believe every person has a story worth hearing. Piano, hiking, deep empathy.", "question": "When was the last time you truly listened to someone?", "category": "philosophy"},
    {"username": "aya_wild", "email": "aya@demo.com", "name": "Aya", "age": 23, "city": "Tel Aviv", "color": "#D32F2F", "bio": "Rock climbing instructor and adventure photographer. Fear is just excitement without breath.", "question": "What scares you and excites you at the same time?", "category": "fears"},
    {"username": "noga_star", "email": "noga@demo.com", "name": "Noga", "age": 30, "city": "Petah Tikva", "color": "#5E35B1", "bio": "Astrophysicist who never lost her sense of wonder. Stargazing, sci-fi, and the big questions.", "question": "If you could know one truth about the universe, what would it be?", "category": "dreams"},
    {"username": "roni_wave", "email": "roni@demo.com", "name": "Roni", "age": 27, "city": "Ashdod", "color": "#0097A7", "bio": "Occupational therapist helping kids shine. Beach volleyball, watercolors, unconditional optimism.", "question": "What does it mean to truly help someone?", "category": "values"},
    {"username": "shaked_earth", "email": "shaked@demo.com", "name": "Shaked", "age": 26, "city": "Tel Aviv", "color": "#388E3C", "bio": "Permaculture farmer building community gardens. Dirt under my nails, peace in my heart. Simple living.", "question": "What do you want to leave behind for the next generation?", "category": "dreams"},
]


def seed_demo_data():
    """Create demo users and profiles if they don't exist."""
    init_database()
    created = 0
    
    for user_data in DEMO_USERS:
        if get_user_by_username(user_data["username"]):
            continue
        
        password_hash = hash_password("demo123")
        user_id = create_user(user_data["username"], user_data["email"], password_hash)
        
        avatar = generate_avatar(user_data["name"], user_data["color"])
        
        create_profile(
            user_id=user_id,
            display_name=user_data["name"],
            age=user_data["age"],
            gender="Female",
            looking_for="Men",
            city=user_data["city"],
            bio=user_data["bio"],
            photos=[avatar],
            insight_question=user_data["question"],
            insight_category=user_data["category"]
        )
        created += 1
    
    # Create a match for user 'dvash' with 'noa_sunshine'
    setup_dvash_match()
    
    return created


def setup_dvash_match():
    """Create a match between dvash and noa_sunshine with conversation history."""
    dvash = get_user_by_username("dvash")
    noa = get_user_by_username("noa_sunshine")
    
    if not dvash or not noa:
        return
    
    dvash_profile = get_profile_by_user_id(dvash['id'])
    noa_profile = get_profile_by_user_id(noa['id'])
    
    if not dvash_profile or not noa_profile:
        return
    
    # Check if interaction already exists
    import sqlite3
    from database.db import get_connection
    
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM interactions WHERE from_user_id = ? AND to_user_id = ?",
            (dvash['id'], noa['id'])
        ).fetchone()
        
        if existing:
            return  # Already set up
        
        # Create mutual interactions (both responded to each other)
        import uuid
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        
        # dvash responds to noa's question
        conn.execute(
            "INSERT INTO interactions (id, from_user_id, to_user_id, insight_response, status, created_at) VALUES (?, ?, ?, ?, 'liked', ?)",
            (str(uuid.uuid4()), dvash['id'], noa['id'], "A perfect Sunday starts with slow coffee on the balcony, a long walk with no destination, and ends with cooking something new while listening to jazz.", now)
        )
        
        # noa responds to dvash's question
        conn.execute(
            "INSERT INTO interactions (id, from_user_id, to_user_id, insight_response, status, created_at) VALUES (?, ?, ?, ?, 'liked', ?)",
            (str(uuid.uuid4()), noa['id'], dvash['id'], "I think vulnerability is the bravest thing a person can show. Being honest about who you are, even when it's uncomfortable.", now)
        )
        
        # Create the match
        match_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO matches (id, user_a_id, user_b_id, matched_at, is_active) VALUES (?, ?, ?, ?, 1)",
            (match_id, dvash['id'], noa['id'], now)
        )
        
        # Add conversation messages
        messages = [
            (noa['id'], "Hey! I loved your answer about Sundays. The jazz + cooking combo sounds perfect 🎶"),
            (dvash['id'], "Thanks! Your answer about vulnerability really resonated with me. It's rare to find someone who values that."),
            (noa['id'], "I think that's what drew me to your profile. Most people hide behind surface-level answers."),
            (dvash['id'], "Exactly. So tell me - what's something vulnerable you've learned about yourself recently?"),
            (noa['id'], "That I'm better at giving advice than taking it 😅 Working on it though. What about you?"),
        ]
        
        for sender_id, content in messages:
            msg_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO messages (id, match_id, sender_id, content, sent_at, read) VALUES (?, ?, ?, ?, ?, 0)",
                (msg_id, match_id, sender_id, content, now)
            )


if __name__ == "__main__":
    count = seed_demo_data()
    print(f"Created {count} demo accounts.")
