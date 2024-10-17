from werkzeug.security import generate_password_hash
from slugify import slugify

fake_competitions = [
    {"name": "Test Competition", "date": "2025-10-22 13:30:00", "available_places": 25},
]

# Mock des clubs
fake_clubs = [
    {"name": "Test Club", "email": "testclub@example.com", "points": 10, "password": generate_password_hash("password123")},
]

club_slug = slugify(fake_clubs[0]['name'], separator='-')
competition_slug = slugify(fake_competitions[0]['name'], separator='-')

print(club_slug)
print(competition_slug)
print(f'/book/{competition_slug}/{club_slug}')
