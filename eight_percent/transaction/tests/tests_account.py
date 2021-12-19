import bcrypt
import jwt
from rest_framework.test import APIClient

from my_settings import HASHING_ALGORITHM, SECRET_KEY
from transaction.models import Account
from users.models import Users
from util.test import BaseTestCase


class AccountTest(BaseTestCase):
    """계좌관련 api 테스트"""

    def setUp(self):
        self.valid_user = Users.objects.create(
            name='elon4856',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        self.unvalid_user = Users.objects.create(
            name='unvalid',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        self.account = Account.objects.create(
            user=self.valid_user,
            password=bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            number="1234-12-123456"
        )

        self.valid_token = "Bearer " + jwt.encode({'id': self.valid_user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
        self.unvalid_token = "Bearer " + jwt.encode({'id': self.unvalid_user.id}, SECRET_KEY,
                                                    algorithm=HASHING_ALGORITHM)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)

    def test_create_account_success(self):
        """계좌개설을 성공했을 시"""

        account_password = {"password": "1234"}

        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_name', response.json())
        self.assertIn('number', response.json())
        self.assertIn('balance', response.json())

    def test_create_account_without_password(self):
        """비밀번호 빈칸으로 계좌개설 요청 시"""

        account_password = {"password": ""}

        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"password": ["This field may not be blank."]})

    def test_create_account_without_token(self):
        """token없이 계좌개설 요청 시"""

        account_password = {"password": "1234"}
        self.client.credentials(HTTP_AUTHORIZATION=False)
        response = self.client.post("/transaction/account", account_password, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "No token"})

    def test_read_account_list_success(self):
        """계좌 list 요청 성공 시"""

        response = self.client.get("/transaction/account")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"number": "1234-12-123456", "balance": 0, "user_name": "elon4856"}])

        self.client.credentials(HTTP_AUTHORIZATION=self.unvalid_token)
        response = self.client.get("/transaction/account")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

