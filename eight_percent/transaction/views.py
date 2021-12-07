from json import JSONDecodeError
from random import randrange

import json
import bcrypt
from datetime import date, timedelta

from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.authentications import BankingAuthentication
from .exceptions import BadRequestException
from .models import Account, Transaction, TransactionType
from utils.decorators import auth_check
from .serializers import AccountSerializer, TransactionSerializer, TransactionModelSerializer


class TransactionHistoryView(View):
    @auth_check
    def get(self, request):
        data = json.loads(request.body)
        page = request.GET.get('page', 1)
        user = request.user
        account_number = data['account_number']
        transaction_type = data['transaction_type']
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date']) + timedelta(days=1)

        start_id = int(start_date.strftime("%Y%m%d")) * 1000000000
        end_id = int(end_date.strftime("%Y%m%d")) * 1000000000
        account_id = Account.objects.get(user=user, number=account_number)

        transaction = Transaction.objects.filter(
            Q(account_id=account_id) & Q(transaction_type=transaction_type) & Q(
                id__range=[start_id, end_id])).order_by('created_at')
        paginated_transaction = Paginator(transaction, 10).get_page(page)
        result = [{
            "transaction_date": transaction.created_at.strftime(r"%Y.%m.%d.%m.%s"),
            "amount"          : transaction.amount,
            "balance"         : transaction.balance,
            "transaction_type": transaction.transaction_type.type,
            "description"     : transaction.description
        } for transaction in paginated_transaction]

        return JsonResponse({'data': result}, status=200)


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
            user   = request.user,
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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response= serializer.save()
        return Response(TransactionModelSerializer(response).data, status=status.HTTP_201_CREATED)


