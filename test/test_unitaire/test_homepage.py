import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage_data_display(client, mocker):
    fake_clubs = [
        {'name': 'Simply Lift', 'email': 'johnsnow@simplylift.co', 'points': '15'},
        {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '8'},
        {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '25'}
    ]
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'
    response = client.get('/homepage')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data


def test_homepage_points_display(client, mocker):
    fake_clubs = [
        {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '15'},
        {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '8'},
        {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '25'}
    ]
    mocker.patch('server.load_clubs', return_value=fake_clubs)

    with client.session_transaction() as session:
        session['email'] = 'john@simplylift.co'

    response = client.get('/homepage')
    assert response.status_code == 200

    simply_lift_points = '15'
    expected_string = f'{simply_lift_points}'
    expected_bytes = expected_string.encode('utf-8')
    assert expected_bytes in response.data


def test_competitions_display(client, mocker):
    fake_clubs = [
        {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '15'},
        {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '8'},
        {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '25'}
    ]

    fake_competitions = [
        {"name": "Spring Festival Test", "date": "2020-03-27 10:00:00", "available_places": "25"},
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "available_places": "18"}
    ]

    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'john@simplylift.co'

    response = client.get('/homepage')
    assert response.status_code == 200

    for competition in fake_competitions:
        assert competition['name'].encode('utf-8') in response.data
        assert competition['date'].encode('utf-8') in response.data
        assert competition['available_places'].encode('utf-8') in response.data


def test_booking_link(client, mocker):
    fake_clubs = [
        {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '15'},
        {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '8'},
        {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '25'}
    ]

    fake_competitions = [
        {"name": "Spring Festival Test", "date": "2020-03-27 10:00:00", "available_places": "25"},
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "available_places": "18"}
    ]

    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'john@simplylift.co'

    response = client.get('/homepage')
    assert response.status_code == 200
