from random import randrange
import bcrypt
from datetime import date, timedelta

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.authentications import BankingAuthentication
from .exceptions import BadRequestException
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

        with transaction.atomic():
            account = Account.objects.select_for_update().get(number=serializer.data.get('account_number'))
            if not bcrypt.checkpw(serializer.data.get('account_password').encode('utf-8'),
                                  account.password.encode('utf-8')):
                raise BadRequestException({'message': '잘못된 비밀번호입니다.'})

            if serializer.data.get('transaction_type') == 1:
                account.balance += serializer.data.get('amount')
            if serializer.data.get('transaction_type') == 2:
                account.balance -= serializer.data.get('amount')
            account.save()
            Transaction(amount=serializer.data.get('amount'),
                        description=serializer.data.get('description'),
                        counterparty=serializer.data.get('counterparty'),
                        account=serializer.data.get('account_number'),
                        transaction_type=serializer.data.get('transaction_type'),
                        balance=account.balance).save()

        return Response( f"transaction 성공하였습니다. {account.balance} 현재 잔액입니다.", status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        page = self.request.query_params.get("page", 1)

        start_date = date.fromisoformat(serializer.data.get('start_date'))
        end_date = date.fromisoformat(serializer.data.get('end_date')) + timedelta(days=1)

        account = Account.objects.get(number=serializer.data.get('account_number'))

        transaction = Transaction.objects.filter(
            Q(account=account.number), Q(transaction_type=serializer.data.get('transaction_type')), Q(
                created_at__range=[start_date, end_date])).order_by('created_at')
        paginated_transaction = Paginator(transaction, 10).get_page(page)
        serializer = TransactionModelSerializer(paginated_transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
