import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


fake_clubs = [
    {"name": "Augustin Verdier",
     "email": "aug.verdier@gmail.com",
     "password": "pbkdf2:sha256:600000$ITQMvxoGGVnBViKH$44439eadd6fe4d08031ce085cdc547ea136684a96270a0206efd76b11abaa362",
     "points": 10},
    {"name": "Test1",
     "email": "test.1@gmail.com",
     "password": "pbkdf2:sha256:600000$BPNAySceUcHVSkmU$31e6d2e35b1143c3324339a091008bcdf6edad45413f2aa1a676c24e02d24c1e",
     "points": 15},
    {"name": "Test2",
     "email": "test.2@gmail.com",
     "password": "test_password",
     "points": 13}
]


def test_button_visibility_when_logged_in(client, mocker):
    # Mock la session pour simuler un utilisateur connecté
    mocker.patch('server.load_clubs', return_value=fake_clubs)

    with client.session_transaction() as session:
        session['email'] = 'test.2@gmail.com'
        session['password'] = 'test_password'

    response = client.get('/homepage')
    assert response.status_code == 200
    assert b'Homepage' in response.data


def test_button_not_visible_when_logged_out(client):
    # Pas de session, donc l'utilisateur est déconnecté
    response = client.get('/homepage')
    assert response.status_code == 302
    assert response.location == '/'
    assert b'Homepage' not in response.data  # Vérifier que le bouton "Home" n'est pas visible
