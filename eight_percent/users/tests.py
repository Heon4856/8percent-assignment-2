import json

import bcrypt
from django.test import Client

from users.models import Users
from util.test import BaseTestCase


class SignUpViewTest(BaseTestCase):
    """회원가입 api 테스트"""

    def setUp(self):
        self.client = Client()

    def test_signup_success(self):
        """회원가입 성공할 경우"""
        user = {
            "name"    : "peter",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})

    def test_signup_with_one_letter_name(self):
        """회원가입시 name을 한글자만 집어넣은 경우"""
        user = {
            "name"    : "p",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': "{'message': '이름을 2자 이상으로 설정해주세요.'}"})

    def test_signup_with_bigger_than_10_letters_name(self):
        """회원가입시 10글자 이상의 name으로 요청한 경우"""
        user = {
            "name"    : "padfadfavdvavadvadv",
            "password": "dlangus1234!"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['Ensure this field has no more than 10 characters.']})

    def test_signup_without_name(self):
        """name 없이 회원가입 요청한 경우"""
        user = {
            "password": "dlangus1234"
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['This field is required.']})

    def test_signup_without_password(self):
        """password 없이 회원가입 요청한 경우"""
        user = {
            "name": "peter",
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'password': ['This field is required.']})

    def test_signup_with_none_password(self):
        """password에 빈칸으로 회원가입 요청한 경우"""
        user = {
            "name"    : "peter",
            "password": ""
        }

        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'password': ['This field may not be blank.']})

    def test_signup_with_existed_name(self):
        """db에 저장된 name으로 회원가입 요청한 경우"""
        user = {
            "name"    : "peter",
            "password": "xkrureo020"
        }

        self.client.post("/users/signup", json.dumps(user), content_type="application/json")
        response = self.client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), { "name": ["users with this name already exists."]})



class LoginTest(BaseTestCase):
    """로그인 api 테스트"""

    def setUp(self):
        Users.objects.create(
            name='elon4856',
            password=bcrypt.hashpw('1234abcd!!!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        self.client = Client()

    def tearDown(self):
        Users.objects.all().delete()

    def test_succecss_login(self):
        """로그인 성공할시 테스트"""

        user = {
            'name'    : 'elon4856',
            'password': '1234abcd!!!!'
        }
        response = self.client.post("/users/login", json.dumps(user), content_type='application/json')
        self.assertIn('Bearer', response.json() )
        self.assertEqual(response.status_code, 200)


    def test_with_not_found_name(self):
        """db에서 찾을 수 없는 name으로 로그인 요청시"""

        user = {
            'name'    : 'aefafdva',
            'password': '1234abcd!!!!!'
        }
        response = self.client.post("/users/login", json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'detail': '찾을 수 없는 이름입니다.'})
        self.assertEqual(response.status_code, 404)

    def test_with_wrong_password(self):
        """db에 저장된 password와 다른 password로 로그인 요청시"""

        user = {
            'name'    : 'elon4856',
            'password': 'wrong_password'
        }
        response = self.client.post("/users/login", json.dumps(user), content_type='application/json')
        self.assertEqual(response.json(), {'detail': '유효하지 않은 비밀번호입니다.'})
        self.assertEqual(response.status_code, 400)