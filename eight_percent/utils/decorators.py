import json
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from users.models import Users
from my_settings import SECRET_KEY, HASHING_ALGORITHM


def auth_check(func):
    def wrapper(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({'message': 'TOKEN_DOES_NOT_EXIST'}, status=400)
            token = token.split()[1]
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            user_id = decoded_auth_token['user_id']
            user = Users.objects.get(id=user_id)

            request.user = user
            return func(self, request)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)

    return wrapper