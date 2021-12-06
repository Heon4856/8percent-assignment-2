import bcrypt
import jwt

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Users
from my_settings import SECRET_KEY, HASHING_ALGORITHM
from .serializers import UserSerializer


class SignUpView(CreateAPIView):
    model = Users
    serializer_class = UserSerializer


class SignInView(APIView):
    def post(self, request, format=None):
        user = Users.objects.get(name=request.data['name'])
        if not user:
            return Response("존재하지 않는 이름입니다.", status=status.HTTP_401_UNAUTHORIZED)
        if not bcrypt.checkpw(request.data["password"].encode('utf-8'), user.password.encode('utf-8')):
            return Response(" 유효하지 않은 비밀번호 ", status=status.HTTP_401_UNAUTHORIZED)
        token = "Bearer " + jwt.encode({'id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
        return Response(token, status=status.HTTP_200_OK)
