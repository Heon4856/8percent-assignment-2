from random import randrange
import bcrypt
from datetime import date, timedelta

from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.authentications import BankingAuthentication
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, TransactionModelSerializer, TransactionListSerializer


class AccountViewSet(GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [BankingAuthentication]

    def create(self, request):
        """
        계좌생성
        POST /accounts/
        data params
        - password
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password')
        account_number = f'3333-{str(randrange(1, 99)).zfill(2)}-{str(randrange(1, 999999)).zfill(6)}'

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        account = Account.objects.create(
            user=request.user,
            password=hashed_password,
            number=account_number,
        )
        return Response(self.get_serializer(account).data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        계좌 리스트 조회
        GET /accounts/
        """
        accounts = Account.objects.filter(user=request.user).all()
        return Response(self.get_serializer(accounts, many=True).data, status=status.HTTP_200_OK)


class TransactionView(GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [BankingAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionSerializer
        if self.action == 'list':
            return TransactionListSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(TransactionModelSerializer(response).data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        page = self.request.query_params.get("page", 1)

        start_date = date.fromisoformat(serializer.data['start_date'])
        end_date = date.fromisoformat(serializer.data['end_date']) + timedelta(days=1)

        account = Account.objects.get(number=serializer.data["account_number"])

        transaction = Transaction.objects.filter(
            Q(account_id=account), Q(transaction_type=serializer.data["transaction_type"]), Q(
                created_at__range=[start_date, end_date])).order_by('created_at')
        paginated_transaction = Paginator(transaction, 10).get_page(page)
        serializer = TransactionModelSerializer(paginated_transaction, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
