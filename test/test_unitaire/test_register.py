import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_registration_route_without_register(client):
    response = client.get('/')  # Simule une requête GET vers la racine '/'
    assert response.status_code == 200


def test_homepage_route_without_register(client):
    response = client.get('/homepage')
    assert response.status_code == 302


@pytest.fixture
def client_in_bdd():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_good_email_registration(client):
    email_in_bdd = 'john@simplylift.co'
    response = client.post('/', data={'email': email_in_bdd})
    assert response.status_code == 302
    assert response.location == '/homepage'


@pytest.fixture
def client_out_of_bdd():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_bad_email_registration(client):
    email_out_of_bdd = 'aug.verdier@gmail.com'
    response = client.post('/', data={'email': email_out_of_bdd})
    assert response.status_code == 302
    assert response.location == '/'
