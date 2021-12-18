import bcrypt
import jwt

from rest_framework.test import APIClient

from my_settings import SECRET_KEY, HASHING_ALGORITHM
from transaction.models import Account
from users.models import Users
from util.test import BaseTestCase

class TransactionTest(BaseTestCase):
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


    def test_create_transaction_success(self):
        transaction_data = {
            "account_number"  : "1234-12-123456",
            "account_password": "1234",
            "amount"          : 10000,
            "description"     : "입금금",
            "counterparty"    : "나",
            "transaction_type": 1
        }

        response = self.client.post("/transaction", transaction_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('transaction 성공하였습니다.', response.json())

    def test_create_transaction_with_wrong_password(self):
        transaction_data = {
            "account_number"  : "1234-12-123456",
            "account_password": "wrong",
            "amount"          : 10000,
            "description"     : "입금금",
            "counterparty"    : "나",
            "transaction_type": 1
        }

        response = self.client.post("/transaction", transaction_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "{'message': '잘못된 비밀번호입니다.'}"})

    def test_create_transaction_with_wrong_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.unvalid_token)

        transaction_data = {
            "account_number"  : "1234-12-123456",
            "account_password": "wrong",
            "amount"          : 10000,
            "description"     : "입금금",
            "counterparty"    : "나",
            "transaction_type": 1

        }

        response = self.client.post("/transaction", transaction_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "{'message': '계좌소유주가 아닙니다.'}"})

    def test_create_transaction_with_minus_balance(self):

        transaction_data = {
            "account_number"  : "1234-12-123456",
            "account_password": "1234",
            "amount"          : 10000,
            "description"     : "입금금",
            "counterparty"    : "나",
            "transaction_type": 2
        }

        response = self.client.post("/transaction", transaction_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "{'message': '잔액보다 출금요청액이 많습니다.'}"})