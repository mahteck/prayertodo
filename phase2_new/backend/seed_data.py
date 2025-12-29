"""
Seed database with sample data for testing
Run with: python3 seed_data.py
"""

from datetime import datetime, timedelta, date
from sqlmodel import Session, select

from database import engine
from models import Masjid, SpiritualTask, DailyHadith, TaskCategory, Priority, Recurrence


def clear_existing_data():
    """Clear all existing data"""
    print("🗑️  Clearing existing data...")
    with Session(engine) as session:
        # Delete in order to respect foreign keys
        session.query(SpiritualTask).delete()
        session.query(DailyHadith).delete()
        session.query(Masjid).delete()
        session.commit()
    print("✅ Existing data cleared\n")


def seed_masjids():
    """Seed sample masjids"""
    print("🕌 Seeding masjids...")

    masjids_data = [
        {
            "name": "Masjid Al-Huda",
            "area": "DHA Phase 5",
            "city": "Karachi",
            "address": "123 Main Street, DHA Phase 5, Karachi",
            "imam_name": "Sheikh Abdullah",
            "phone": "+92-300-1234567",
            "facilities": "Prayer hall, Wudu area, Islamic library, Quran classes",
        },
        {
            "name": "Masjid Al-Noor",
            "area": "Gulshan-e-Iqbal",
            "city": "Karachi",
            "address": "Block 13-D, Gulshan-e-Iqbal, Karachi",
            "imam_name": "Mufti Yusuf",
            "phone": "+92-300-2345678",
            "facilities": "Prayer hall, Madrasah, Community center",
        },
        {
            "name": "Masjid Al-Raheem",
            "area": "Clifton",
            "city": "Karachi",
            "address": "Block 4, Clifton, Karachi",
            "imam_name": "Sheikh Ahmed",
            "phone": "+92-300-3456789",
            "facilities": "Prayer hall, Parking, Women's section",
        },
        {
            "name": "Masjid Al-Fattah",
            "area": "Saddar",
            "city": "Karachi",
            "address": "Empress Market Road, Saddar, Karachi",
            "imam_name": "Maulana Ibrahim",
            "phone": "+92-300-4567890",
            "facilities": "Prayer hall, Wudu area",
        },
        {
            "name": "Masjid Al-Taqwa",
            "area": "North Nazimabad",
            "city": "Karachi",
            "address": "Block L, North Nazimabad, Karachi",
            "imam_name": "Sheikh Muhammad",
            "phone": "+92-300-5678901",
            "facilities": "Prayer hall, Islamic school, Library",
        },
    ]

    with Session(engine) as session:
        for data in masjids_data:
            masjid = Masjid(**data)
            session.add(masjid)
            session.commit()
            session.refresh(masjid)
            print(f"  ✓ Created: {masjid.name}")

    print(f"✅ {len(masjids_data)} masjids seeded\n")


def seed_tasks():
    """Seed sample spiritual tasks"""
    print("📋 Seeding spiritual tasks...")

    with Session(engine) as session:
        # Get masjids for associations
        masjids = session.exec(select(Masjid)).all()

        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        next_week = now + timedelta(days=7)

        tasks_data = [
            {
                "title": "Attend Fajr at Masjid Al-Huda",
                "description": "Join congregation for Fajr prayer",
                "category": TaskCategory.FARZ,
                "priority": Priority.URGENT,
                "masjid_id": masjids[0].id if masjids else None,
                "due_datetime": tomorrow.replace(hour=5, minute=30),
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Memorize Surah Al-Mulk",
                "description": "Memorize 5 verses of Surah Al-Mulk daily",
                "category": TaskCategory.NAFL,
                "priority": Priority.HIGH,
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Donate to local charity",
                "description": "Make sadaqah donation this week",
                "category": TaskCategory.DEED,
                "priority": Priority.MEDIUM,
                "due_datetime": next_week,
                "recurrence": Recurrence.WEEKLY,
            },
            {
                "title": "Friday Jummah Prayer at Masjid Al-Noor",
                "description": "Attend Friday congregation prayer",
                "category": TaskCategory.FARZ,
                "priority": Priority.URGENT,
                "masjid_id": masjids[1].id if len(masjids) > 1 else None,
                "due_datetime": now.replace(hour=13, minute=0),
                "recurrence": Recurrence.WEEKLY,
            },
            {
                "title": "Read Quran for 30 minutes",
                "description": "Daily Quran recitation with translation",
                "category": TaskCategory.SUNNAH,
                "priority": Priority.HIGH,
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Tahajjud Prayer",
                "description": "Pray 8 rakats of Tahajjud in last third of night",
                "category": TaskCategory.NAFL,
                "priority": Priority.HIGH,
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Visit sick friend at hospital",
                "description": "Part of caring for the sick (visiting rights)",
                "category": TaskCategory.DEED,
                "priority": Priority.MEDIUM,
                "due_datetime": tomorrow.replace(hour=16, minute=0),
            },
            {
                "title": "Attend Islamic lecture at Masjid Al-Raheem",
                "description": "Weekly knowledge session on Friday nights",
                "category": TaskCategory.NAFL,
                "priority": Priority.MEDIUM,
                "masjid_id": masjids[2].id if len(masjids) > 2 else None,
                "due_datetime": now.replace(hour=20, minute=0),
                "recurrence": Recurrence.WEEKLY,
            },
            {
                "title": "Make Dhikr after Fajr",
                "description": "100 times SubhanAllah, Alhamdulillah, Allahu Akbar",
                "category": TaskCategory.SUNNAH,
                "priority": Priority.HIGH,
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Study Hadith collection",
                "description": "Read 5 hadith from Sahih Bukhari with commentary",
                "category": TaskCategory.NAFL,
                "priority": Priority.MEDIUM,
                "recurrence": Recurrence.DAILY,
            },
            {
                "title": "Prepare Iftar for family (Ramadan)",
                "description": "Cook and arrange Iftar meal",
                "category": TaskCategory.DEED,
                "priority": Priority.HIGH,
                "tags": "Ramadan, Family, Cooking",
            },
            {
                "title": "Taraweeh Prayer at Masjid Al-Taqwa",
                "description": "20 rakats Taraweeh during Ramadan",
                "category": TaskCategory.SUNNAH,
                "priority": Priority.HIGH,
                "masjid_id": masjids[4].id if len(masjids) > 4 else None,
                "recurrence": Recurrence.DAILY,
                "tags": "Ramadan, Prayer",
            },
            {
                "title": "Learn 5 new Arabic words",
                "description": "Improve Quranic Arabic vocabulary",
                "category": TaskCategory.OTHER,
                "priority": Priority.LOW,
                "recurrence": Recurrence.DAILY,
                "tags": "Learning, Arabic",
            },
            {
                "title": "Help clean the masjid",
                "description": "Volunteer for masjid cleaning duty",
                "category": TaskCategory.DEED,
                "priority": Priority.MEDIUM,
                "masjid_id": masjids[0].id if masjids else None,
                "due_datetime": next_week,
                "recurrence": Recurrence.WEEKLY,
            },
        ]

        for data in tasks_data:
            task = SpiritualTask(**data)
            session.add(task)
            session.commit()
            session.refresh(task)
            print(f"  ✓ Created: {task.title[:50]}...")

    print(f"✅ {len(tasks_data)} spiritual tasks seeded\n")


def seed_hadith():
    """Seed daily hadith entries"""
    print("📖 Seeding daily hadith...")

    hadith_data = [
        {
            "hadith_date": date.today(),
            "arabic_text": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ",
            "english_translation": "Whoever believes in Allah and the Last Day should speak good or remain silent.",
            "narrator": "Abu Hurairah",
            "source": "Sahih Bukhari 6018",
            "theme": "Speech",
        },
        {
            "hadith_date": date.today() + timedelta(days=1),
            "arabic_text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ",
            "english_translation": "Verily, actions are judged by intentions.",
            "narrator": "Umar ibn Al-Khattab",
            "source": "Sahih Bukhari 1",
            "theme": "Intention",
        },
        {
            "hadith_date": date.today() + timedelta(days=2),
            "arabic_text": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ",
            "english_translation": "The Muslim is the one from whose tongue and hand the Muslims are safe.",
            "narrator": "Abdullah ibn Amr",
            "source": "Sahih Bukhari 10",
            "theme": "Character",
        },
        {
            "hadith_date": date.today() + timedelta(days=3),
            "arabic_text": "الدِّينُ النَّصِيحَةُ",
            "english_translation": "Religion is sincerity (nasihah).",
            "narrator": "Tamim Ad-Dari",
            "source": "Sahih Muslim 55",
            "theme": "Sincerity",
        },
        {
            "hadith_date": date.today() + timedelta(days=4),
            "arabic_text": "مَنْ صَلَّى الْفَجْرَ فَهُوَ فِي ذِمَّةِ اللَّهِ",
            "english_translation": "Whoever prays Fajr is under the protection of Allah.",
            "narrator": "Jundub ibn Abdullah",
            "source": "Sahih Muslim 657",
            "theme": "Prayer",
        },
    ]

    with Session(engine) as session:
        for data in hadith_data:
            hadith = DailyHadith(**data)
            session.add(hadith)
            session.commit()
            session.refresh(hadith)
            print(f"  ✓ Created hadith for: {hadith.hadith_date}")

    print(f"✅ {len(hadith_data)} hadith entries seeded\n")


def main():
    """Main seeding function"""
    print("=" * 60)
    print("  🌱 SalaatFlow Database Seeding")
    print("=" * 60 + "\n")

    clear_existing_data()
    seed_masjids()
    seed_tasks()
    seed_hadith()

    print("=" * 60)
    print("✅ Database seeding completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
