# 💜 Yuval Itzhaki - Deep-Value Matching Dating App

> Where Deep Values Create Real Connections

Unlike traditional swipe-based dating apps, Yuval Itzhaki focuses on **Deep-Value Matching** through **The Insight Layer** - a personality-based question that must be answered before a full profile is revealed.

## How It Works

1. **Create Your Profile** - Set up info, photos, and choose your unique Insight Question
2. **Discover** - Browse profiles showing only a photo and their insight question
3. **Engage** - Write a thoughtful response to unlock their full profile
4. **Match** - When both users respond to each other's insights, it's a match!
5. **Connect** - Chat freely with your matches

## Quick Start

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub repo `dvashtom/yuval-itzhaki`
2. Go to https://share.streamlit.io/
3. Click "New app" -> Select repo -> Main file: `app.py` -> Deploy

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Streamlit (Python) |
| Database | SQLite |
| Auth | bcrypt password hashing |
| Deployment | Streamlit Cloud |

## Project Structure
```
├── app.py              # Main entry point
├── config/settings.py  # Constants & preset questions
├── auth/               # Authentication
├── database/db.py      # SQLite CRUD operations
├── pages/              # Discovery, Profile, Matches
├── utils/              # Helpers & matching algorithm
├── components/         # Reusable UI components
└── assets/style.css    # Custom styling
```

## Security
- Passwords hashed with bcrypt
- Parameterized SQL queries (no injection)
- Session-based authentication
- Input validation on all forms
