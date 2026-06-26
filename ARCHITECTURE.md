# Architecture & Data Schema - Yuval Itzhaki

## Data Schema (JSON Structure for User Profile)

### Users Table
```json
{
  "id": "uuid",
  "username": "string (unique)",
  "email": "string (unique)",
  "password_hash": "string (bcrypt)",
  "created_at": "ISO timestamp",
  "last_active": "ISO timestamp",
  "is_active": true
}
```

### Profiles Table
```json
{
  "id": "uuid",
  "user_id": "uuid (FK -> users.id)",
  "display_name": "string",
  "age": 25,
  "gender": "Male | Female | Non-binary | Other",
  "looking_for": "Men | Women | Everyone",
  "city": "string",
  "bio": "string (max 500 chars)",
  "photos": ["base64_encoded_image_1", "base64_encoded_image_2"],
  "insight_question": "What does a perfect Sunday look like for you?",
  "insight_category": "values | fears | dreams | lifestyle | philosophy",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

### Interactions Table (Insight Responses)
```json
{
  "id": "uuid",
  "from_user_id": "uuid (who responded)",
  "to_user_id": "uuid (whose question was answered)",
  "insight_response": "string (the actual answer)",
  "status": "pending | liked | passed",
  "created_at": "ISO timestamp"
}
```

### Matches Table
```json
{
  "id": "uuid",
  "user_a_id": "uuid",
  "user_b_id": "uuid",
  "matched_at": "ISO timestamp",
  "is_active": true
}
```

### Messages Table
```json
{
  "id": "uuid",
  "match_id": "uuid (FK -> matches.id)",
  "sender_id": "uuid (FK -> users.id)",
  "content": "string",
  "sent_at": "ISO timestamp",
  "read": false
}
```

## The Insight Layer - Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. REGISTRATION                                         │
│     User creates account + profile                       │
│     User selects/writes their INSIGHT QUESTION           │
│     (from 5 categories: values, fears, dreams,           │
│      lifestyle, philosophy)                               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  2. DISCOVERY FEED                                       │
│     User sees other profiles in LOCKED state:            │
│     - First photo visible                                │
│     - Name, age, city visible                            │
│     - Insight Question visible                           │
│     - Bio and full details HIDDEN                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  3. ENGAGEMENT GATE                                      │
│     User MUST write a thoughtful response                │
│     (minimum 10 characters) to the insight question      │
│     OR skip the profile                                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  4. PROFILE UNLOCK                                       │
│     After responding, full profile is revealed:          │
│     - All photos                                         │
│     - Full bio                                           │
│     - Complete details                                   │
│     The response is saved as an "interaction"            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  5. MUTUAL MATCHING                                      │
│     When BOTH users respond to each other's questions:   │
│     → A MATCH is automatically created                   │
│     → Both users are notified                            │
│     → Chat becomes available                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  6. CONVERSATION                                         │
│     Matched users can chat freely                        │
│     The conversation is seeded by the insight responses  │
│     both users already provided                          │
└─────────────────────────────────────────────────────────┘
```

## Technical Decisions

| Decision | Reasoning |
|----------|-----------|
| SQLite over Supabase | Zero-config for Streamlit Cloud deployment; no external DB needed for MVP |
| bcrypt for passwords | Industry standard; resistant to rainbow table attacks |
| Base64 photos in DB | Avoids need for cloud storage (S3/GCS) in MVP; photos resized to 500x500 |
| Session state for auth | Native Streamlit approach; no cookies needed |
| Modular file structure | Easy to swap SQLite for Supabase later without rewriting logic |

## Migration Path to Production
1. Replace SQLite with Supabase (change only `database/db.py`)
2. Add OAuth via Streamlit-Authenticator
3. Move photos to Supabase Storage
4. Add real-time websocket for chat
