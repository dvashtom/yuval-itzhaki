"""Database operations for Yuval Itzhaki Dating App using SQLite."""

import sqlite3
import os
import uuid
import json
from datetime import datetime
from contextlib import contextmanager
from config.settings import DB_PATH


def get_db_path():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return DB_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_active TEXT,
                is_active INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                looking_for TEXT NOT NULL,
                city TEXT,
                bio TEXT,
                photos TEXT DEFAULT '[]',
                insight_question TEXT NOT NULL,
                insight_category TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS interactions (
                id TEXT PRIMARY KEY,
                from_user_id TEXT NOT NULL,
                to_user_id TEXT NOT NULL,
                insight_response TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY (from_user_id) REFERENCES users(id),
                FOREIGN KEY (to_user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS matches (
                id TEXT PRIMARY KEY,
                user_a_id TEXT NOT NULL,
                user_b_id TEXT NOT NULL,
                matched_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_a_id) REFERENCES users(id),
                FOREIGN KEY (user_b_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                match_id TEXT NOT NULL,
                sender_id TEXT NOT NULL,
                content TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                FOREIGN KEY (match_id) REFERENCES matches(id),
                FOREIGN KEY (sender_id) REFERENCES users(id)
            );
        """)


def create_user(username, email, password_hash):
    user_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, created_at, last_active) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, email, password_hash, now, now)
        )
    return user_id


def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None


def get_user_by_email(email):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def create_profile(user_id, display_name, age, gender, looking_for, city, bio, photos, insight_question, insight_category):
    profile_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO profiles (id, user_id, display_name, age, gender, looking_for, city, bio, photos, insight_question, insight_category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (profile_id, user_id, display_name, age, gender, looking_for, city, bio, json.dumps(photos), insight_question, insight_category, now, now)
        )
    return profile_id


def get_profile_by_user_id(user_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
        if row:
            profile = dict(row)
            profile['photos'] = json.loads(profile['photos'])
            return profile
        return None


def update_profile(user_id, **kwargs):
    if 'photos' in kwargs:
        kwargs['photos'] = json.dumps(kwargs['photos'])
    kwargs['updated_at'] = datetime.utcnow().isoformat()
    set_clause = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values()) + [user_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE profiles SET {set_clause} WHERE user_id = ?", values)
    return True


def get_discovery_profiles(current_user_id, gender_filter=None):
    with get_connection() as conn:
        interacted = conn.execute(
            "SELECT to_user_id FROM interactions WHERE from_user_id = ?", (current_user_id,)
        ).fetchall()
        interacted_ids = [row['to_user_id'] for row in interacted]
        interacted_ids.append(current_user_id)
        placeholders = ",".join("?" * len(interacted_ids))
        query = f"""SELECT p.*, u.username FROM profiles p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id NOT IN ({placeholders}) AND u.is_active = 1"""
        params = list(interacted_ids)
        if gender_filter and gender_filter != "Everyone":
            gender_map = {"Men": "Male", "Women": "Female"}
            query += " AND p.gender = ?"
            params.append(gender_map.get(gender_filter, gender_filter))
        query += " ORDER BY RANDOM() LIMIT 20"
        rows = conn.execute(query, params).fetchall()
        profiles = []
        for row in rows:
            profile = dict(row)
            profile['photos'] = json.loads(profile['photos'])
            profiles.append(profile)
        return profiles


def create_interaction(from_user_id, to_user_id, insight_response):
    interaction_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO interactions (id, from_user_id, to_user_id, insight_response, status, created_at) VALUES (?, ?, ?, ?, 'pending', ?)",
            (interaction_id, from_user_id, to_user_id, insight_response, now)
        )
    check_and_create_match(from_user_id, to_user_id)
    return interaction_id


def get_interactions_for_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT i.*, p.display_name, p.photos, p.bio, p.age, p.city
            FROM interactions i JOIN profiles p ON i.from_user_id = p.user_id
            WHERE i.to_user_id = ? AND i.status = 'pending' ORDER BY i.created_at DESC""",
            (user_id,)
        ).fetchall()
        interactions = []
        for row in rows:
            interaction = dict(row)
            interaction['photos'] = json.loads(interaction['photos'])
            interactions.append(interaction)
        return interactions


def update_interaction_status(interaction_id, status):
    with get_connection() as conn:
        conn.execute("UPDATE interactions SET status = ? WHERE id = ?", (status, interaction_id))


def check_and_create_match(user_a_id, user_b_id):
    with get_connection() as conn:
        reverse = conn.execute(
            "SELECT id FROM interactions WHERE from_user_id = ? AND to_user_id = ? AND status != 'passed'",
            (user_b_id, user_a_id)
        ).fetchone()
        if reverse:
            existing = conn.execute(
                "SELECT id FROM matches WHERE (user_a_id = ? AND user_b_id = ?) OR (user_a_id = ? AND user_b_id = ?)",
                (user_a_id, user_b_id, user_b_id, user_a_id)
            ).fetchone()
            if not existing:
                match_id = str(uuid.uuid4())
                now = datetime.utcnow().isoformat()
                conn.execute("INSERT INTO matches (id, user_a_id, user_b_id, matched_at) VALUES (?, ?, ?, ?)",
                    (match_id, user_a_id, user_b_id, now))
                return True
    return False


def get_matches_for_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT m.*, CASE WHEN m.user_a_id = ? THEN m.user_b_id ELSE m.user_a_id END as other_user_id
            FROM matches m WHERE (m.user_a_id = ? OR m.user_b_id = ?) AND m.is_active = 1
            ORDER BY m.matched_at DESC""",
            (user_id, user_id, user_id)
        ).fetchall()
        matches = []
        for row in rows:
            match = dict(row)
            other_profile = get_profile_by_user_id(match['other_user_id'])
            if other_profile:
                match['other_profile'] = other_profile
                last_msg = conn.execute(
                    "SELECT content, sent_at, sender_id FROM messages WHERE match_id = ? ORDER BY sent_at DESC LIMIT 1",
                    (match['id'],)
                ).fetchone()
                match['last_message'] = dict(last_msg) if last_msg else None
                matches.append(match)
        return matches


def send_message(match_id, sender_id, content):
    msg_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        conn.execute("INSERT INTO messages (id, match_id, sender_id, content, sent_at) VALUES (?, ?, ?, ?, ?)",
            (msg_id, match_id, sender_id, content, now))
    return msg_id


def get_messages(match_id):
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT m.*, p.display_name FROM messages m
            JOIN profiles p ON m.sender_id = p.user_id
            WHERE m.match_id = ? ORDER BY m.sent_at ASC""",
            (match_id,)
        ).fetchall()
        return [dict(row) for row in rows]
