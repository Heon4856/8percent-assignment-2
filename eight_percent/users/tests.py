import json

import bcrypt
from django.test import Client, TestCase

from users.models import Users


class SignUpViewTest(TestCase):
    def test_signup_success(self):
        client = Client()

        user = {
            "name": "peter",
            "password": "dlangus1234!"
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})


    def test_signup_valueerror(self):
        client = Client()

        response = client.post("/users/signup")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'JSON_DECODE_ERROR'})

    def test_signup_wrong_name_format(self):
        client = Client()

        user = {
            "name": "p",
            "password": "dlangus1234!"
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_NAME_FORMAT'})


    def test_signup_wrong_password_format(self):
        client = Client()

        user = {
            "name": "peter",
            "password": "dlangus1234"
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_PASSWORD_FORMAT'})

    def setUp(self):
        Users.objects.create(
            name="peter",
            password="dlangus1234^"
        )

    def tearDown(self):
        Users.objects.all().delete()


class LoginTest(TestCase):
    def setUp(self):
        Users.objects.create(
            name='안다민',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        Users.objects.all().delete()

    def test_succecss_login(self):
        user = {
            'name': '안다민',
            'password': '1234abcd!!!!'
        }
        client = Client()
        response = client.post("/users/login", json.dumps(user), content_type='application/json')
        self.assertEqual(response.json().get('message'), 'SUCCESS')

    def test_failed_login(self):
        user = {
            'name': '가나다',
            'password': '1234abcd!!!!!'
        }
        client = Client()
        response = client.post("/users/login", json.dumps(user), content_type='application/json')
        self.assertEqual(response.json().get('message'), 'USER_DOES_NOT_EXIST')