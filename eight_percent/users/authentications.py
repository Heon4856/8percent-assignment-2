import jwt
from rest_framework import authentication

from .models import Users
from ..my_settings import SECRET_KEY, HASHING_ALGORITHM

class BankingAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get('Authorization')
        if access_token:
            access_token = access_token[len("Bearer "):]
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            userid = payload['id']
            user = Users.objects.get(id=userid)
            return user, None
        return None