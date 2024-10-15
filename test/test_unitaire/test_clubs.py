import pytest
from werkzeug.security import generate_password_hash
from server import app


fake_clubs = [
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret$"), "points": 13},
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret$"), "points": 13},
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret$"), "points": 13}
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


def test_login_of_an_unidentified_user(client):
    response = client.get('/clubs')
    assert response.status_code == 200


def test_login_of_an_identified_user(client):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/clubs')
    assert response.status_code == 200


def test_club_name_display(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/homepage')
    assert response.status_code == 200

    for club in fake_clubs:
        assert club['name'].encode('utf-8') in response.data


def test_club_points_display(client, mock_clubs):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/homepage')
    assert response.status_code == 200

    for club in fake_clubs:
        assert str(club['points']).encode('utf-8') in response.data

