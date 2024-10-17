import pytest
from server import app
from slugify import slugify
from flask import request


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


fake_clubs = [
        {'name': 'Simply Lift', 'email': 'johnsnow@simplylift.co', 'points': 2},
    ]

fake_competitions = [
    {'name': 'Spring Festival Test', 'date': '2020-03-27 10:00:00', 'available_places': 5},
]


def test_competition_name_display(client, mocker):

    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'
    competition_name = (slugify(competition['name'], separator='-') for competition in fake_competitions)
    clean_competition_name = list(competition_name)
    club_name = (slugify(club['name'], separator='-') for club in fake_clubs)
    clean_club_name = list(club_name)

    for comp, club in zip(clean_competition_name, clean_club_name):
        response = client.get(f'/book/{comp}/{club}')
        assert response.status_code == 200
        assert b'Spring Festival Test' in response.data


def test_competition_point_display(client, mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'
    competition_name = (slugify(competition['name'], separator='-') for competition in fake_competitions)
    clean_competition_name = list(competition_name)
    club_name = (slugify(club['name'], separator='-') for club in fake_clubs)
    clean_club_name = list(club_name)
    for comp, club in zip(clean_competition_name, clean_club_name):
        response = client.get(f'/book/{comp}/{club}')
        assert response.status_code == 200
        assert b'5' in response.data


def test_negative_point_competition(client, mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'
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
            'places': 100
        }
        response = client.post('/booking', data=fake_data)
        assert response.status_code == 302


def test_negativ_ask_from_club(client, mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'
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
            'places': -3
        }
        response = client.post('/booking', data=fake_data)
        assert response.status_code == 302


def test_too_high_ask_from_club(client, mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)
    mocker.patch('server.load_competitions', return_value=fake_competitions)

    with client.session_transaction() as session:
        session['email'] = 'johnsnow@simplylift.co'

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
