import pytest
from server import app
from werkzeug.security import generate_password_hash
from slugify import slugify

# Fixtures
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


fake_competitions = [
    {"name": "Test Competition", "date": "2025-10-22 13:30:00", "available_places": 25},
]

# Mock des clubs
fake_clubs = [
    {"name": "Test Club", "email": "testclub@example.com", "points": 10, "password": generate_password_hash("password123")},
]

@pytest.fixture
def mock_data(mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)


def test_booking(client, mock_data):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    competition_name = (slugify(competition['name'], separator='-') for competition in fake_competitions)
    clean_competition_name = list(competition_name)
    club_name = (slugify(club['name'], separator='-') for club in fake_clubs)
    clean_club_name = list(club_name)

    for comp, club in zip(clean_competition_name, clean_club_name):
        response = client.get(f'/book/{comp}/{club}')
        assert response.status_code == 200

        fake_data = {
            'competition': fake_competitions[0]['name'],
            'club': fake_clubs[0]['name'],
            'places': 3
        }
        response = client.post('/booking', data=fake_data)
        assert response.status_code == 302

        follow_response = client.get(response.location, follow_redirects=True)
        assert b"competition has been taken into account." in follow_response.data
