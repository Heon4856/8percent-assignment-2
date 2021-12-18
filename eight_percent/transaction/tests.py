import bcrypt
import jwt
from rest_framework.test import APIClient

from my_settings import SECRET_KEY, HASHING_ALGORITHM
from users.models import Users
from util.test import BaseTestCase


class AccountTest(BaseTestCase):
    def setUp(self):
        self.valid_user = Users.objects.create(
            name='elon4856',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        self.unvalid_user = Users.objects.create(
            name='unvalid',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        self.valid_token = "Bearer " + jwt.encode({'id': self.valid_user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
        self.unvalid_token = "Bearer " + jwt.encode({'id': self.unvalid_user.id}, SECRET_KEY,
                                                    algorithm=HASHING_ALGORITHM)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)

    def test_create_account_success(self):
        account_password = {"password": "1234"}

        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_name', response.json())
        self.assertIn('number', response.json())
        self.assertIn('balance', response.json())

    def test_create_account_without_password(self):
        account_password = {"password": ""}

        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"password": ["This field may not be blank."]})

    def test_create_account_without_token(self):
        account_password = {"password": "1234"}
        self.client.credentials(HTTP_AUTHORIZATION=False)
        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "No token"})