import pytest
from server import app
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


fake_clubs = [
    {"name": "Test club", "email": "test.club@email.com", "password": generate_password_hash("TestPassword123"), "points": 13},
]


@pytest.fixture
def mock_clubs(mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)


def test_login(client, mock_clubs):
    response = client.post('/', data={
        'form_type': 'login',
        'email': 'test.club@email.com',
        'password': 'TestPassword123'
    })

    assert response.status_code == 302
    assert response.location == '/homepage'

    follow_response = client.get(response.location, follow_redirects=True)
    assert b"Welcome, Test club" in follow_response.data
