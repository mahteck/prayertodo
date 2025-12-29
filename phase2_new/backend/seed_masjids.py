"""
Seed script to populate sample masjids for testing.

Usage:
    cd backend
    python seed_masjids.py
"""

from sqlmodel import Session, create_engine, select
from models import Masjid
from config import settings

def seed_masjids():
    """Add sample masjids to database."""

    engine = create_engine(settings.database_url)

    sample_masjids = [
        {
            "name": "Masjid Al-Huda",
            "area_name": "DHA Phase 5",
            "city": "Karachi",
            "address": "123 Main Street, DHA Phase 5",
            "imam_name": "Maulana Abdul Rahman",
            "phone": "+92-300-1234567",
            "latitude": 24.8607,
            "longitude": 67.0011,
            "fajr_time": "05:30",
            "dhuhr_time": "13:00",
            "asr_time": "16:30",
            "maghrib_time": "18:15",
            "isha_time": "19:45",
            "jummah_time": "13:30"
        },
        {
            "name": "Masjid Al-Noor",
            "area_name": "Gulshan-e-Iqbal Block 13",
            "city": "Karachi",
            "address": "456 Block 13, Gulshan-e-Iqbal",
            "fajr_time": "05:25",
            "dhuhr_time": "12:55",
            "asr_time": "16:25",
            "maghrib_time": "18:10",
            "isha_time": "19:40",
            "jummah_time": "13:15"
        },
        {
            "name": "Jamia Masjid Clifton",
            "area_name": "Clifton Block 2",
            "city": "Karachi",
            "address": "Sea View Road, Clifton",
            "imam_name": "Maulana Ahmad Shah",
            "phone": "+92-333-5555555",
            "latitude": 24.8167,
            "longitude": 67.0299,
            "fajr_time": "05:35",
            "dhuhr_time": "13:05",
            "asr_time": "16:35",
            "maghrib_time": "18:20",
            "isha_time": "19:50",
            "jummah_time": "13:15"
        },
        {
            "name": "Masjid Bilal",
            "area_name": "Malir Cantt",
            "city": "Karachi",
            "address": "Malir Cantonment Area",
            "fajr_time": "05:20",
            "dhuhr_time": "12:50",
            "asr_time": "16:20",
            "maghrib_time": "18:05",
            "isha_time": "19:35"
        },
        {
            "name": "Baitul Mukarram",
            "area_name": "Bahadurabad",
            "city": "Karachi",
            "imam_name": "Maulana Ishaq Ali",
            "phone": "+92-321-8888888",
            "fajr_time": "05:29",
            "dhuhr_time": "12:59",
            "asr_time": "16:29",
            "maghrib_time": "18:14",
            "isha_time": "19:44",
            "jummah_time": "13:00"
        }
    ]

    with Session(engine) as session:
        # Check if masjids already exist
        existing = session.exec(select(Masjid)).first()
        if existing:
            print("⚠️  Masjids already exist. Skipping seed.")
            return

        # Add sample masjids
        for masjid_data in sample_masjids:
            masjid = Masjid(**masjid_data)
            session.add(masjid)

        session.commit()
        print(f"✅ Seeded {len(sample_masjids)} masjids successfully!")

if __name__ == "__main__":
    seed_masjids()
