from json import JSONDecodeError
from random import randrange

import json
import jwt
import bcrypt
from datetime import date, timedelta
import time

from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Account, Transaction, TransactionType
from utils.decorators import auth_check


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


class CreateAccountView(View):
    # 유저 계좌번호 생성
    @auth_check
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user
            password = data['password']
            account_number = f'3333-{str(randrange(1, 99)).zfill(2)}-{str(randrange(1, 999999)).zfill(6)}'

            if not password:
                return JsonResponse({'message': 'ENTER_YOUR_PASSWORD'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
            Account.objects.create(
                user     = user,
                password = hashed_password,
                number   = account_number,
            )
            return JsonResponse({'message': 'SUCCESS', 'account_number' : f'{account_number}'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)


class LookupAccountView(View):
    # 유저가 가지고 있는 계좌번호만 조회
    @auth_check
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            accounts = Account.objects.filter(user_id=user)
            account_list = [item.number for item in accounts]
            return JsonResponse({'account_list': account_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)


class TransactionView(View):
    @auth_check
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user
            account_number = data['account_number']
            account_password = data['account_password']
            amount = data['amount']
            description = data['description']
            counterparty = data['counterparty']
            transaction_type_id = data['transaction_type_id']

            hashed_account_number = bcrypt.hashpw(account_password.encode('utf-8'), bcrypt.gensalt())
            account = Account.objects.select_for_update().get( number=account_number)


            if not bcrypt.checkpw(account_password.encode('utf-8'), hashed_account_number):
                return JsonResponse({'message': 'INVALID_YOUR_PASSWORD'})
            if not account_number:
                return JsonResponse({'message': 'ENTER_YOUR_ACCOUNT_NUMBER'}, status=400)
            if not amount or amount < 0:
                return JsonResponse({'message': 'ENTER_YOUR_AMOUNT'}, status=400)
            if not counterparty:
                return JsonResponse({'message': 'ENTER_YOUR_COUNTERPARTY'}, status=400)
            if not transaction_type_id:
                return JsonResponse({'message': 'ENTER_YOUR_TRANSACTION_TYPE'}, status=400)
            if not account:
                return JsonResponse({'message': 'INVALID_YOUR_ACCOUNT_NUMBER'}, status=400)

            with transaction.atomic():
                # transaction_type이 1일경우 입금
                if transaction_type_id == 1:
                    Transaction.objects.create(
                        amount=amount,
                        description=description,
                        counterparty=counterparty,
                        account_id=account.id,
                        transaction_type_id=1
                    )
                    account.balance = account.balance + amount
                    account.save()

                # transaction_type이 2일경우 출금
                elif transaction_type_id == 2:
                    if account.balance - amount < 0:
                        return JsonResponse({'message': 'INSUFFICIENT_IS_AMOUNT.'})
                    Transaction.objects.create(
                        amount=amount,
                        description=description,
                        counterparty=counterparty,
                        account_id=account.id,
                        transaction_type_id=2
                    )
                    account.balance = account.balance - amount
                    account.save()

                return JsonResponse({'message': 'SUCCESS', "balance": account.balance}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)
