"""
SalaatFlow Phase II - Database Seed Data

Populates the database with sample data for testing and demonstration.
Run this script after creating the database tables.

Usage:
    python3 seed_data.py
"""

from datetime import datetime, timedelta
from sqlmodel import Session, select

from database import engine
from models import (
    SpiritualTask, Masjid, DailyHadith,
    TaskCategory, Priority, Recurrence
)


def clear_existing_data(session: Session) -> None:
    """Clear all existing data from the database."""
    print("🗑️  Clearing existing data...")

    # Delete in order to respect foreign key constraints
    for task in session.exec(select(SpiritualTask)).all():
        session.delete(task)

    for masjid in session.exec(select(Masjid)).all():
        session.delete(masjid)

    for hadith in session.exec(select(DailyHadith)).all():
        session.delete(hadith)

    session.commit()
    print("✅ Existing data cleared")


def seed_masjids(session: Session) -> dict:
    """Create sample masjid data."""
    print("🕌 Seeding masjids...")

    masjids_data = [
        {
            "name": "Masjid Al-Huda",
            "area": "DHA Phase 5",
            "city": "Karachi",
            "address": "123 Main Boulevard, DHA Phase 5",
            "imam_name": "Imam Abdullah Khan",
            "phone": "+92-300-1234567"
        },
        {
            "name": "Masjid Al-Noor",
            "area": "Gulshan-e-Iqbal",
            "city": "Karachi",
            "address": "Block 13-D, Gulshan-e-Iqbal",
            "imam_name": "Imam Muhammad Usman",
            "phone": "+92-321-9876543"
        },
        {
            "name": "Central Jamia Masjid",
            "area": "Clifton",
            "city": "Karachi",
            "address": "Sea View Avenue, Clifton",
            "imam_name": "Imam Ahmed Hassan",
            "phone": "+92-333-5555555"
        },
        {
            "name": "Masjid Al-Farooq",
            "area": "Malir",
            "city": "Karachi",
            "address": "Malir Cantt Area",
            "imam_name": "Imam Bilal Siddiqui",
            "phone": "+92-345-7777777"
        },
        {
            "name": "Masjid Baitul Mukarram",
            "area": "North Nazimabad",
            "city": "Karachi",
            "address": "Block L, North Nazimabad",
            "imam_name": "Imam Tariq Jamil",
            "phone": "+92-312-8888888"
        },
    ]

    masjids = {}
    for data in masjids_data:
        masjid = Masjid(**data)
        masjid.created_at = datetime.utcnow()
        masjid.updated_at = datetime.utcnow()
        session.add(masjid)
        session.commit()
        session.refresh(masjid)
        masjids[data["name"]] = masjid
        print(f"  ✓ Created: {masjid.name}")

    print(f"✅ {len(masjids)} masjids seeded")
    return masjids


def seed_tasks(session: Session, masjids: dict) -> None:
    """Create sample spiritual task data."""
    print("📋 Seeding spiritual tasks...")

    now = datetime.utcnow()
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    tasks_data = [
        # Farz tasks
        {
            "title": "Attend Fajr prayer at Masjid Al-Huda",
            "description": "Wake up 30 minutes early for tahajjud and wudu",
            "category": TaskCategory.FARZ,
            "priority": Priority.URGENT,
            "masjid_id": masjids["Masjid Al-Huda"].id,
            "due_datetime": today + timedelta(days=1, hours=5, minutes=30),
            "recurrence": Recurrence.DAILY,
            "completed": False,
            "tags": "prayer,fajr,masjid"
        },
        {
            "title": "Attend Jummah prayer",
            "description": "Friday congregation prayer at Central Jamia Masjid",
            "category": TaskCategory.FARZ,
            "priority": Priority.URGENT,
            "masjid_id": masjids["Central Jamia Masjid"].id,
            "due_datetime": today + timedelta(days=(4 - today.weekday()) % 7, hours=13),
            "recurrence": Recurrence.WEEKLY,
            "completed": False,
            "tags": "prayer,jummah,congregation"
        },
        {
            "title": "Pray Dhuhr at office",
            "description": "Set reminder 10 minutes before prayer time",
            "category": TaskCategory.FARZ,
            "priority": Priority.HIGH,
            "due_datetime": today + timedelta(hours=13, minutes=30),
            "recurrence": Recurrence.DAILY,
            "completed": False,
            "tags": "prayer,dhuhr,office"
        },

        # Sunnah tasks
        {
            "title": "Recite Ayat-ul-Kursi before sleep",
            "description": "Part of bedtime Sunnah practices",
            "category": TaskCategory.SUNNAH,
            "priority": Priority.MEDIUM,
            "due_datetime": today + timedelta(hours=23),
            "recurrence": Recurrence.DAILY,
            "completed": False,
            "tags": "quran,sunnah,bedtime"
        },
        {
            "title": "Read Surah Al-Kahf",
            "description": "Friday Sunnah - read Surah Al-Kahf",
            "category": TaskCategory.SUNNAH,
            "priority": Priority.MEDIUM,
            "due_datetime": today + timedelta(days=(4 - today.weekday()) % 7),
            "recurrence": Recurrence.WEEKLY,
            "completed": False,
            "tags": "quran,sunnah,friday"
        },
        {
            "title": "Pray Tahajjud",
            "description": "Night prayer in last third of night",
            "category": TaskCategory.SUNNAH,
            "priority": Priority.MEDIUM,
            "due_datetime": today + timedelta(days=1, hours=4),
            "recurrence": Recurrence.DAILY,
            "completed": False,
            "tags": "prayer,tahajjud,night"
        },

        # Nafl tasks
        {
            "title": "Perform I'tikaf at Masjid Al-Noor",
            "description": "Last 10 days of Ramadan I'tikaf",
            "category": TaskCategory.NAFL,
            "priority": Priority.LOW,
            "masjid_id": masjids["Masjid Al-Noor"].id,
            "tags": "itikaf,ramadan,masjid"
        },
        {
            "title": "Fast on Monday",
            "description": "Voluntary fasting - Sunnah of Prophet (ﷺ)",
            "category": TaskCategory.NAFL,
            "priority": Priority.LOW,
            "due_datetime": today + timedelta(days=(0 - today.weekday()) % 7),
            "recurrence": Recurrence.WEEKLY,
            "completed": False,
            "tags": "fasting,voluntary,sunnah"
        },
        {
            "title": "Perform Duha prayer",
            "description": "Mid-morning voluntary prayer (2-8 rakats)",
            "category": TaskCategory.NAFL,
            "priority": Priority.LOW,
            "due_datetime": today + timedelta(hours=9),
            "recurrence": Recurrence.DAILY,
            "completed": False,
            "tags": "prayer,duha,voluntary"
        },

        # Deed tasks
        {
            "title": "Give charity to local food bank",
            "description": "Donate to Masjid Al-Farooq food program",
            "category": TaskCategory.DEED,
            "priority": Priority.MEDIUM,
            "masjid_id": masjids["Masjid Al-Farooq"].id,
            "due_datetime": today + timedelta(days=3),
            "completed": False,
            "tags": "charity,sadaqah,helping"
        },
        {
            "title": "Visit sick neighbor",
            "description": "Check on elderly neighbor and bring groceries",
            "category": TaskCategory.DEED,
            "priority": Priority.HIGH,
            "due_datetime": today + timedelta(days=1, hours=16),
            "completed": False,
            "tags": "kindness,neighbor,visit"
        },
        {
            "title": "Teach Quran class at masjid",
            "description": "Saturday morning children's Quran class",
            "category": TaskCategory.DEED,
            "priority": Priority.MEDIUM,
            "masjid_id": masjids["Masjid Baitul Mukarram"].id,
            "due_datetime": today + timedelta(days=(5 - today.weekday()) % 7, hours=9),
            "recurrence": Recurrence.WEEKLY,
            "completed": False,
            "tags": "teaching,quran,children"
        },

        # Some completed tasks
        {
            "title": "Attended Fajr prayer",
            "description": "Completed Fajr at Masjid Al-Huda",
            "category": TaskCategory.FARZ,
            "priority": Priority.URGENT,
            "masjid_id": masjids["Masjid Al-Huda"].id,
            "due_datetime": today + timedelta(hours=5, minutes=30),
            "completed": True,
            "tags": "prayer,fajr,masjid"
        },
        {
            "title": "Read Surah Yaseen",
            "description": "Friday morning recitation",
            "category": TaskCategory.SUNNAH,
            "priority": Priority.MEDIUM,
            "due_datetime": today + timedelta(hours=8),
            "completed": True,
            "tags": "quran,yaseen,friday"
        },
    ]

    for data in tasks_data:
        task = SpiritualTask(**data)
        task.created_at = now
        task.updated_at = now
        session.add(task)
        print(f"  ✓ Created: {task.title[:50]}...")

    session.commit()
    print(f"✅ {len(tasks_data)} spiritual tasks seeded")


def seed_hadith(session: Session) -> None:
    """Create sample daily hadith data."""
    print("📖 Seeding daily hadith...")

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    hadith_data = [
        {
            "date": today,
            "arabic_text": "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
            "english_translation": "Actions are judged by intentions, and everyone will get what was intended.",
            "reference": "Sahih Bukhari 1",
            "narrator": "Umar ibn Al-Khattab (RA)"
        },
        {
            "date": today - timedelta(days=1),
            "arabic_text": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الْآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ",
            "english_translation": "Whoever believes in Allah and the Last Day should speak good or remain silent.",
            "reference": "Sahih Bukhari 6018",
            "narrator": "Abu Hurairah (RA)"
        },
        {
            "date": today - timedelta(days=2),
            "arabic_text": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ",
            "english_translation": "A Muslim is one from whose tongue and hand other Muslims are safe.",
            "reference": "Sahih Bukhari 10",
            "narrator": "Abdullah ibn Amr (RA)"
        },
        {
            "date": today + timedelta(days=1),
            "arabic_text": "لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ",
            "english_translation": "None of you truly believes until he loves for his brother what he loves for himself.",
            "reference": "Sahih Bukhari 13",
            "narrator": "Anas ibn Malik (RA)"
        },
        {
            "date": today + timedelta(days=2),
            "arabic_text": "الْمُؤْمِنُ الْقَوِيُّ خَيْرٌ وَأَحَبُّ إِلَى اللَّهِ مِنْ الْمُؤْمِنِ الضَّعِيفِ",
            "english_translation": "The strong believer is better and more beloved to Allah than the weak believer.",
            "reference": "Sahih Muslim 2664",
            "narrator": "Abu Hurairah (RA)"
        },
    ]

    for data in hadith_data:
        hadith = DailyHadith(**data)
        hadith.created_at = datetime.utcnow()
        session.add(hadith)
        print(f"  ✓ Created hadith for: {data['date'].strftime('%Y-%m-%d')}")

    session.commit()
    print(f"✅ {len(hadith_data)} hadith entries seeded")


def main():
    """Main seeding function."""
    print("\n" + "=" * 60)
    print("  SalaatFlow Phase II - Database Seeding")
    print("=" * 60 + "\n")

    with Session(engine) as session:
        # Clear existing data
        clear_existing_data(session)

        # Seed in order (respecting foreign keys)
        masjids = seed_masjids(session)
        seed_tasks(session, masjids)
        seed_hadith(session)

    print("\n" + "=" * 60)
    print("  ✅ Database seeding completed successfully!")
    print("=" * 60 + "\n")
    print("You can now:")
    print("  1. Start the API server: uvicorn main:app --reload")
    print("  2. View the data at: http://localhost:8000/docs")
    print("\n")


if __name__ == "__main__":
    main()
