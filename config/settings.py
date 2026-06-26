"""Application settings and constants."""

APP_NAME = "Yuval Itzhaki"
APP_TAGLINE = "Where Deep Values Create Real Connections"
APP_VERSION = "1.0.0"
DB_PATH = "data/yuval_itzhaki.db"
MAX_PHOTOS = 3
MAX_BIO_LENGTH = 500
MAX_INSIGHT_RESPONSE_LENGTH = 300
MIN_AGE = 18
MAX_AGE = 99

INSIGHT_CATEGORIES = {
    "values": "Core Values & Beliefs",
    "fears": "Fears & Vulnerabilities",
    "dreams": "Dreams & Aspirations",
    "lifestyle": "Lifestyle & Daily Life",
    "philosophy": "Philosophy & Worldview",
}

PRESET_INSIGHT_QUESTIONS = {
    "values": [
        "What principle would you never compromise on, even if it cost you everything?",
        "If you could instill one value in every person on Earth, what would it be?",
        "What does loyalty mean to you in a relationship?",
    ],
    "fears": [
        "What is your biggest fear, and how do you face it?",
        "What's the scariest thing you've ever done that turned out to be worth it?",
        "What keeps you up at night?",
    ],
    "dreams": [
        "If money wasn't an issue, how would you spend your days?",
        "What's a dream you've never told anyone about?",
        "Where do you see yourself in 10 years - honestly, not ideally?",
    ],
    "lifestyle": [
        "What does a perfect Sunday look like for you?",
        "What's your non-negotiable daily ritual?",
        "How do you recharge after a tough week?",
    ],
    "philosophy": [
        "What's a belief you held strongly that you've since changed your mind about?",
        "Do you think people can truly change? Why or why not?",
        "What's the meaning of life, in your own words?",
    ],
}

GENDER_OPTIONS = ["Male", "Female", "Non-binary", "Other"]
LOOKING_FOR_OPTIONS = ["Men", "Women", "Everyone"]
