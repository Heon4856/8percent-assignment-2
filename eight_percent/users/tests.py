import json

import bcrypt
from django.test import Client

from users.models import Users
from util.test import BaseTestCase


class SignUpViewTest(BaseTestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_success(self):
        user = {
            "name"    : "peter",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})

    def test_signup_with_one_letter_name(self):
        user = {
            "name"    : "p",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': "{'message': '이름을 2자 이상으로 설정해주세요.'}"})

    def test_signup_with_bigger_than_10_letters_name(self):
        user = {
            "name"    : "padfadfavdvavadvadv",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  {'name': ['Ensure this field has no more than 10 characters.']})

    def test_signup_without_name(self):
        user = {
            "password": "dlangus1234"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['This field is required.']})

    def test_signup_without_password(self):
        user = {
            "name": "peter",
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'password': ['This field is required.']})


    def test_signup_with_none_password(self):
        user = {
            "name"    : "peter",
            "password": ""
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'password': ['This field may not be blank.']})
