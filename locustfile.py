from locust import HttpUser, task, between
import pytest


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def clubs_as_unconnected_user(self):
        response = self.client.get('/clubs')
        assert response.status_code == 200

    @task
    def invalid_email_register(self):
        response = self.client.post('/',
                                    data={'form_type': 'register',
                                          'name': 'TestLocust', 'email': 'test.locust.gmail.com',
                                          'password': 'TestLocust.1998'})
        assert response.status_code == 302

    @task
    def valid_register(self):
        response = self.client.post('/',
                                    data={'form_type': 'register',
                                          'name': 'TestLocust', 'email': 'test.locust@gmail.com',
                                          'password': 'TestLocust.1998'})
        assert response.status_code == 302

    @task
    def valid_login(self):
        response = self.client.post('/',
                                    data={'form_type': 'login',
                                          'email': 'test.locust@gmail.com', 'password': 'TestLocust.1998'})
        assert response.status_code == 302

    @task
    def invalid_login(self):
        response = self.client.post('/',
                                    data={'form_type': 'login', 'email': 'wrong.email@gmail.com',
                                          'password': 'WrongPassword123'})
        assert response.status_code == 302

    @task
    def homepage(self):
        response = self.client.get('/homepage')
        assert response.status_code == 200

    @task
    def clubs_as_connected_user(self):
        response = self.client.get('/clubs')
        assert response.status_code == 200

    @task
    def booking(self):
        club = 'testlocust'
        competition = 'testlocust-competition'
        response = self.client.get(f'book/{competition}/{club}')
        assert response.status_code == 200

    @task
    def logout(self):
        response = self.client.get('/logout')
        assert response.status_code == 302

    @task
    def register_and_login(self):
        self.clubs_as_unconnected_user()
        self.invalid_email_register()
        self.valid_register()
        self.invalid_login()
        self.valid_login()
        self.homepage()
        self.clubs_as_connected_user()
        self.logout()
