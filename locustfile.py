from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def clubs_as_unconnected_user(self):
        self.client.get('/clubs')

    @task
    def invalid_email_register(self):
        self.client.post('/',
                         data={'form_type': 'register',
                               'name': 'TestLocust', 'email': 'test.locust.gmail.com',
                               'password': 'TestLocust.1998'})

    @task
    def valid_register(self):
        self.client.post('/',
                         data={'form_type': 'register',
                               'name': 'TestLocust', 'email': 'test.locust@gmail.com',
                               'password': 'TestLocust.1998'})

    @task
    def valid_login(self):
        self.client.post('/',
                         data={'form_type': 'login',
                               'email': 'test.locust@gmail.com', 'password': 'TestLocust.1998'})

    @task
    def invalid_login(self):
        self.client.post('/',
                         data={'form_type': 'login', 'email': 'wrong.email@gmail.com',
                               'password': 'WrongPassword123'})

    @task
    def homepage(self):
        self.client.get('/homepage')

    @task
    def clubs_as_connected_user(self):
        self.client.get('/clubs')

    @task
    def booking(self):
        club = 'testlocust'
        competition = 'testlocust-competition'
        self.client.get(f'book/{competition}/{club}')

    @task
    def logout(self):
        self.client.get('/logout')

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
