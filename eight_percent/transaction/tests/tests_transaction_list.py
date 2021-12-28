import json
from datetime import datetime

import bcrypt
import jwt
from rest_framework.test import APIClient

from my_settings import HASHING_ALGORITHM, SECRET_KEY
from transaction.models import Account
from users.models import Users
from util.test import BaseTestCase


class TransactionListTest(BaseTestCase):
    """거래내역 갖고오기 test"""
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
        transaction_data = {
            "account_number"  : "1234-12-123456",
            "account_password": "1234",
            "amount"          : 10000,
            "description"     : "입금금",
            "counterparty"    : "나",
            "transaction_type": 1
        }

        self.client.post("/transaction", transaction_data, format='json')

    def test_read_transaction_list_success(self):
        """거래내역 리스트를 성공적으로 가져올 경우"""
        today = datetime.today().strftime("%Y-%m-%d")
        search_data = {
            'account_number'  : "1234-12-123456",
            'account_password': "1234",
            'transaction_type': "1",
            'start_date'      : today,
            'end_date'        : today
        }
        response = self.client.generic(method="GET", path="/transaction", data=json.dumps(search_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('account', response.json()[0])
        self.assertIn('amount', response.json()[0])
        self.assertIn('description', response.json()[0])
        self.assertIn('counterparty', response.json()[0])
        self.assertIn('transaction_type', response.json()[0])
