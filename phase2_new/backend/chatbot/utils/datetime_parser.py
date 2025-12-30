"""
DateTime Parsing Utility
Parses natural language date/time expressions and prayer-relative times
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
import re


def parse_relative_date(text: str) -> datetime:
    """
    Parse relative date expressions like "tomorrow", "today", "tonight"

    Args:
        text: Natural language date expression

    Returns:
        datetime object for the specified date

    Examples:
        >>> from datetime import datetime, timedelta
        >>> result = parse_relative_date("tomorrow")
        >>> result.day == (datetime.now() + timedelta(days=1)).day
        True
    """
    text_lower = text.lower().strip()
    now = datetime.now()

    if "tomorrow" in text_lower or "kal" in text_lower:
        return now + timedelta(days=1)
    elif "today" in text_lower or "aaj" in text_lower:
        return now
    elif "tonight" in text_lower:
        return now.replace(hour=20, minute=0, second=0, microsecond=0)
    else:
        # Default to today
        return now


def parse_prayer_relative_time(
    prayer: str,
    minutes_offset: int,
    direction: str,
    masjid_times: dict,
    target_date: Optional[datetime] = None
) -> datetime:
    """
    Calculate datetime relative to prayer time

    Args:
        prayer: Prayer name (Fajr, Dhuhr, Asr, Maghrib, Isha, Jummah)
        minutes_offset: Number of minutes to offset
        direction: "before" or "after"
        masjid_times: Dict with prayer times (e.g., {"fajr_time": "05:30"})
        target_date: Optional date to use (defaults to today)

    Returns:
        datetime calculated from prayer time ± offset

    Examples:
        >>> masjid_times = {"fajr_time": "05:30"}
        >>> result = parse_prayer_relative_time("Fajr", 20, "before", masjid_times)
        >>> result.hour == 5 and result.minute == 10
        True
    """
    if target_date is None:
        target_date = datetime.now()

    # Get prayer time field name
    prayer_field = f"{prayer.lower()}_time"

    if prayer_field not in masjid_times:
        raise ValueError(f"Prayer time not found for {prayer}")

    # Parse time string (HH:MM format)
    prayer_time_str = masjid_times[prayer_field]
    hour, minute = map(int, prayer_time_str.split(':'))

    # Create datetime for prayer
    prayer_datetime = target_date.replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )

    # Apply offset
    if direction == "before":
        result = prayer_datetime - timedelta(minutes=minutes_offset)
    else:  # "after"
        result = prayer_datetime + timedelta(minutes=minutes_offset)

    return result


def extract_time_from_text(text: str) -> Optional[Tuple[int, int]]:
    """
    Extract time from text like "5:30 AM", "1:00 PM", "17:30"

    Args:
        text: Text containing time

    Returns:
        Tuple of (hour, minute) or None if not found

    Examples:
        >>> extract_time_from_text("5:30 AM")
        (5, 30)
        >>> extract_time_from_text("1:00 PM")
        (13, 0)
        >>> extract_time_from_text("17:30")
        (17, 30)
    """
    # Pattern for 12-hour format (5:30 AM, 1:00 PM)
    pattern_12h = r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)'
    match = re.search(pattern_12h, text)

    if match:
        hour, minute, period = match.groups()
        hour = int(hour)
        minute = int(minute)

        # Convert to 24-hour format
        if period.upper() == 'PM' and hour != 12:
            hour += 12
        elif period.upper() == 'AM' and hour == 12:
            hour = 0

        return (hour, minute)

    # Pattern for 24-hour format (17:30)
    pattern_24h = r'(\d{1,2}):(\d{2})'
    match = re.search(pattern_24h, text)

    if match:
        hour, minute = match.groups()
        return (int(hour), int(minute))

    return None


def parse_datetime_expression(text: str, context: Optional[dict] = None) -> Optional[datetime]:
    """
    Parse complex datetime expressions

    Args:
        text: Natural language datetime expression
        context: Optional context dict (masjid_times, etc.)

    Returns:
        datetime object or None

    Examples:
        >>> result = parse_datetime_expression("tomorrow at 5:30 AM")
        >>> result is not None
        True
    """
    text_lower = text.lower().strip()

    # Check for relative dates
    base_date = parse_relative_date(text)

    # Check for explicit time
    time_tuple = extract_time_from_text(text)
    if time_tuple:
        hour, minute = time_tuple
        return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Check for "in X hours/minutes"
    in_pattern = r'in\s+(\d+)\s+(hour|hours|minute|minutes)'
    match = re.search(in_pattern, text_lower)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        if 'hour' in unit:
            return datetime.now() + timedelta(hours=amount)
        else:  # minutes
            return datetime.now() + timedelta(minutes=amount)

    # Default to base date at midnight
    return base_date.replace(hour=0, minute=0, second=0, microsecond=0)
