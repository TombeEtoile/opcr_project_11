import pytest
from server import app


# Fixtures
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Mock des données de compétition
fake_competitions = [
    {"name": "Competition 1", "date": "2025-03-27 10:00:00", "available_places": 25},
]


@pytest.fixture
def mock_competitions(mocker):
    mocker.patch('server.load_competitions', return_value=fake_competitions)


def test_registration(client):
    response = client.post('/', data={
        'form_type': 'register',
        'name': 'Test Club',
        'email': 'testclub@example.com',
        'password': 'TestPassword123'
    })

    assert response.status_code == 302
    assert response.location == '/'
