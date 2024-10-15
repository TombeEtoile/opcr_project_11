import pytest
from werkzeug.security import generate_password_hash
from server import app

# FAKE BDD
fake_clubs = [
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret"), "points": 13}
]


# CLIENT TEST
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# BDD MOCK
@pytest.fixture
def mock_clubs(mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)


def test_session_pop(client):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/logout')
    assert response.status_code == 302

    with client.session_transaction() as session:
        assert 'email' not in session


def test_redirection(client):
    with client.session_transaction() as session:
        session['email'] = fake_clubs[0]['email']

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.location == '/'
