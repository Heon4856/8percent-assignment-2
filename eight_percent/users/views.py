import bcrypt
import jwt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from my_settings import HASHING_ALGORITHM, SECRET_KEY
from .exceptions import NotFoundException, WrongPasswordException
from .models import Users
from .serializers import UserSerializer


class SignUpView(CreateAPIView):
    """
    회원가입 관련 view
    """
    model = Users
    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        회원가입 api
        POST /users/signup
        data params
        - name
        - password
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    """
    로그인 관련 view
    """
    def post(self, request: Request) -> Response:
        """
        로그인 api
        POST /users/login
        data params
        - name
        - password
        """
        try:
            user = Users.objects.get(name=request.data['name'])
        except Exception:
            raise NotFoundException("찾을 수 없는 이름입니다.")
        if not bcrypt.checkpw(request.data["password"].encode('utf-8'), user.password.encode('utf-8')):
            raise WrongPasswordException("유효하지 않은 비밀번호입니다.")

        token = "Bearer " + jwt.encode({'id': user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
        return Response(token, status=status.HTTP_200_OK)
