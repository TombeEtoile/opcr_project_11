import pytest
from werkzeug.security import generate_password_hash
from server import app
from slugify import slugify


fake_clubs = [
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret$"), "points": 13}
]


fake_competitions = [
        {"name": "Test name 2", "date": "2025-10-22 13:30:00", "available_places": 18}
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


# BDD CLUBS COMPETITION
@pytest.fixture
def mock_competition(mocker):
    mocker.patch('server.load_clubs', return_value=fake_competitions)


# ---------------------------------------------- TEST NOT CONNECTED USER ----------------------------------------------
def test_navbar_login_and_register_not_connected_user(client):
    response = client.get('/')
    assert response.status_code == 200

    assert b'Clubs list' in response.data
    assert b'Register as a competition' in response.data


def test_navbar_display_competition_registration_not_connected_user(client):
    response = client.get('/competition_registration')
    assert response.status_code == 200

    assert b'Clubs list' in response.data
    assert b'Register as a club' in response.data


def test_navbar_display_clubs_not_connected_user(client):
    response = client.get('/clubs')
    assert response.status_code == 200

    assert b'Register as a club' in response.data
    assert b'Register as a competition' in response.data


# ------------------------------------------------ TEST CONNECTED USER ------------------------------------------------
def test_navbar_display_login_and_register_connected_user(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/')
    assert response.status_code == 200

    assert b'Homepage' in response.data
    assert b'Clubs list' in response.data
    assert b'Logout' in response.data


def test_navbar_display_competition_registration_connected_user(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/')
    assert response.status_code == 200

    assert b'Homepage' in response.data
    assert b'Clubs list' in response.data
    assert b'Logout' in response.data


def test_navbar_display_homepage_connected_user(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/homepage')
    assert response.status_code == 200

    assert b'Homepage' in response.data
    assert b'Clubs list' in response.data
    assert b'Logout' in response.data


def test_navbar_display_clubs_connected_user(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/clubs')
    assert response.status_code == 200

    assert b'Homepage' in response.data
    assert b'Logout' in response.data


def test_navbar_display_booking_connected_user(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    club_name = slugify(fake_clubs[0]['name'], separator='-')
    competition_name = slugify(fake_competitions[0]['name'], separator='-')

    # MODIFIER PAR URL DES CLUBS
    response = client.get(f'/book/{club_name}/{competition_name}')
    assert response.status_code == 200

    assert b'Homepage' in response.data
    assert b'Clubs list' in response.data
    assert b'Logout' in response.data
