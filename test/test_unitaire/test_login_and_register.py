import pytest
from werkzeug.security import generate_password_hash
from server import app

# FAKE BDD
fake_clubs = [
    {"name": "Test name", "email": "test@email.co", "password": generate_password_hash("secret"), "points": 13}
]

# DATA IN BDD
name_in_bdd = 'Test name'
email_in_bdd = 'test@email.co'
password_in_bdd = 'secret'

# DATA OUT OF BDD
name_out_of_bdd = 'Bad name'
email_out_of_bdd = 'bad.email@email.co'
password_out_of_bdd = 'bad.password'

# BAD DATA
bad_email = 'bad.email.email.com'
bad_password = 'badpassword'


# BDD MOCK
@pytest.fixture
def mock_clubs(mocker):
    mocker.patch('server.load_clubs', return_value=fake_clubs)


# CLIENT TEST
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ------------------------------------------------ TEST LOGIN ------------------------------------------------
def test_registration_route_without_register(client):
    response = client.get('/')
    assert response.status_code == 200


def test_homepage_route_without_register(client):
    response = client.get('/homepage')
    assert response.status_code == 302
    assert response.location == '/'


def test_good_login(client, mock_clubs):

    response = client.post('/', data={'form_type': 'login', 'email': email_in_bdd, 'password': password_in_bdd})
    assert response.status_code == 302
    assert response.location == '/homepage'


def test_bad_login(client, mock_clubs):

    response = client.post('/',
                           data={'form_type': 'login', 'email': email_out_of_bdd, 'password': password_out_of_bdd})
    assert response.status_code == 302
    assert response.location == '/'


# ------------------------------------------------ TEST REGISTRATION ------------------------------------------------
def test_good_registration(client, mock_clubs):

    response = client.post('/',
                           data={'form_type': 'register',
                                 'name': name_out_of_bdd, 'email': email_out_of_bdd, 'password': password_out_of_bdd})

    assert response.status_code == 302
    assert response.location == '/'


def test_registration_with_already_use_email(client, mock_clubs):
    response = client.post('/',
                           data={'form_type': 'register',
                                 'name': name_out_of_bdd, 'email': email_in_bdd, 'password': password_out_of_bdd})

    assert response.status_code == 302
    assert response.location == '/'


def test_registration_without_email(client, mock_clubs):
    response = client.post('/',
                           data={'form_type': 'register',
                                 'name': name_out_of_bdd, 'email': '', 'password': password_out_of_bdd})

    assert response.status_code == 302
    assert response.location == '/'


def test_registration_email_without_at(client, mock_clubs):
    response = client.post('/',
                           data={'form_type': 'register',
                                 'name': name_out_of_bdd, 'email': bad_email, 'password': password_out_of_bdd})

    assert response.status_code == 302
    assert response.location == '/'


def test_registration_with_bad_password(client, mock_clubs):
    response = client.post('/',
                           data={'form_type': 'register',
                                 'name': name_out_of_bdd, 'email': email_out_of_bdd, 'password': bad_password})

    assert response.status_code == 302
    assert response.location == '/'
