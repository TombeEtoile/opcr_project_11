import pytest
from werkzeug.security import generate_password_hash
from datetime import datetime
from server import app
from slugify import slugify


fake_clubs = [
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret$"), "points": 13},
]


fake_competitions = [
        {"name": "Test name 1", "date": "2020-10-22 13:30:00", "available_places": 13},
        {"name": "Test name 2", "date": "2025-10-22 13:30:00", "available_places": 18},
    ]


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# BDD CLUBS MOCK
@pytest.fixture
def mock_clubs(mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)


# BDD COMPETITIONS MOCK
@pytest.fixture
def mock_competitions(mocker):
    mocker.patch('server.load_competitions', return_value=fake_competitions)


def test_homepage_data_display(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']
    response = client.get('/homepage')
    assert response.status_code == 200

    for club in fake_clubs:
        assert club['name'].encode('utf-8') in response.data


def test_homepage_points_display(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/homepage')
    assert response.status_code == 200

    for club in fake_clubs:
        assert str(club['points']).encode('utf-8') in response.data


def test_competitions_display(client, mock_clubs, mock_competitions):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/homepage')
    assert response.status_code == 200

    good_competitions = []
    for competition in fake_competitions:
        competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date >= datetime.now():
            good_competitions.append(competition['name'])

    assert fake_competitions[0]['name'].encode('utf-8') not in response.data
    assert fake_competitions[1]['name'].encode('utf-8') in response.data


def test_booking_link(client, mock_clubs, mock_competitions):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    club_name = slugify(fake_clubs[0]['name'], separator='-')
    competition_name = slugify(fake_competitions[1]['name'], separator='-')

    response = client.get('/homepage')
    assert response.status_code == 200

    expected_link = f'/book/{competition_name}/{club_name}'
    assert b'Book my place' in response.data
    assert expected_link.encode('utf-8') in response.data
