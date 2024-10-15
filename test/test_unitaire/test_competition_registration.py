import pytest
from server import app

# FAKE BDD
fake_competitions = [
        {"name": "Competition 1", "date": "2020-03-27 10:00:00", "available_places": 25},
        {"name": "Competition 2", "date": "2025-10-22 13:30:00", "available_places": 18}
    ]


# FAKE DATA
good_date = '2025-10-22'
time = '13:30:00'
wrong_date = '2020-05-27'
number = '18'
negative_number = '-3'
zero_number = '0'


# BDD MOCK
@pytest.fixture
def mock_competitions(mocker):
    mocker.patch('server.load_competitions', return_value=fake_competitions)


# CLIENT TEST
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ------------------------------------------ TEST COMPETITION REGISTRATION ------------------------------------------

def test_competition_registration_route_without_register(client):
    response = client.get('/competition_registration')
    assert response.status_code == 200


def test_wrong_date(client, mock_competitions):
    response = client.post('/competition_registration',
                           data={'name': 'Test competition', 'date': wrong_date, 'time': time, 'available_places': number})
    assert response.status_code == 302
    assert response.location == '/competition_registration'


def test_negative_available_places(client, mock_competitions):
    response = client.post('/competition_registration',
                           data={'name': 'Test competition', 'date': good_date, 'time': time, 'available_places': negative_number})
    assert response.status_code == 302
    assert response.location == '/competition_registration'


def test_0_available_places(client, mock_competitions):
    response = client.post('/competition_registration',
                           data={'name': 'Test competition', 'date': good_date, 'time': time, 'available_places': zero_number})
    assert response.status_code == 302
    assert response.location == '/competition_registration'
