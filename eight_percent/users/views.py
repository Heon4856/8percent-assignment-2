import json
import bcrypt
import jwt
import re
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models import Users
from my_settings import SECRET_KEY, HASHING_ALGORITHM


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = Users.objects.get(name=data['name'])
            password = data['password']

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
                return JsonResponse({'token': token, 'message': 'SUCCESS'}, status=200)
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=401)


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data['name']
            password = data['password']

            if not name or not password:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)

            p_name = re.compile(r'^[가-힣a-zA-Z]{2,20}$')
            p_password = re.compile(r'^(?=.*[!-/:-@])(?!.*[ㄱ-ㅣ가-힣]).{8,20}$')

            if not p_name.match(name):
                return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=400)
            if not p_password.match(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)


            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')

            Users.objects.create(
                name=name,
                password=decoded_hashed_pw,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)