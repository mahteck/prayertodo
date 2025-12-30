"""
Language Detection Utility
Detects whether user message is in English or Urdu/Roman Urdu
"""


def detect_language(user_message: str) -> str:
    """
    Detects language (English or Urdu/Roman Urdu) from user message

    Args:
        user_message: The user's input text

    Returns:
        "en" for English, "ur" for Urdu/Roman Urdu

    Examples:
        >>> detect_language("Show me today's hadith")
        'en'
        >>> detect_language("Aaj ka hadith sunao")
        'ur'
        >>> detect_language("Fajr ka time kya hai?")
        'ur'
        >>> detect_language("Add a task to pray")
        'en'
    """
    urdu_keywords = [
        "aaj", "kal", "ka", "kya", "hai", "mujhe", "sunao",
        "do", "bana", "se", "pehle", "baad", "mein", "main",
        "namaz", "sadaqah", "karna", "chahiye", "dikhaao",
        "batao", "chahte", "hain", "liye", "wale", "nahi",
        "koi", "kitni", "kitne", "kahan", "kis", "bare"
    ]

    message_lower = user_message.lower()
    urdu_count = sum(1 for keyword in urdu_keywords if keyword in message_lower)

    # If 2 or more Urdu keywords found, consider it Urdu
    return "ur" if urdu_count >= 2 else "en"
