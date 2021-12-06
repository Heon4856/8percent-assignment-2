import json
import bcrypt
import jwt
import re
from json import JSONDecodeError
from rest_framework.generics import CreateAPIView

from django.views import View
from django.http  import JsonResponse

from .models import Users
from my_settings import SECRET_KEY, HASHING_ALGORITHM
from .serializers import UserSerializer


class SignUpView(CreateAPIView):
    model = Users
    serializer_class = UserSerializer



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

