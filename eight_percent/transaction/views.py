from json           import JSONDecodeError
from random         import randrange

import json
import jwt
import bcrypt

from django.views   import View
from django.http    import JsonResponse
from django.db      import transaction

from .models import Account, Transaction


class CreateAccountView(View):
    # 유저 계좌번호 생성
    # @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data           = json.loads(request.body)
            user           = request.user
            password       = data['password']
            account_number = f'3333-{str(randrange(1,99)).zfill(2)}-{str(randrange(1,999999)).zfill(6)}'

            if not password:
                return JsonResponse({'message': 'ENTER_YOUR_PASSWORD'}, status=400)

            hashed_password       = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_account_number = bcrypt.hashpw(account_number.encode('utf-8'), bcrypt.gensalt())

            Account.objects.create(
                user     = user,
                password = hashed_password,
                number   = hashed_account_number,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)


class LookupAccountView(View)
    #유저가 가지고 있는 계좌번호만 조회
    # @login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user         = request.user
            accounts     = Account.objects.get(user_id = user)
            account_list = [accounts.number for number in accounts]
            return JsonResponse({'account_list': account_list}, status= 200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)


class TransactionView(View):
    # @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data                = json.loads(request.body)
            user                = request.user
            account_number      = data['account_number']
            account_password    = data['account_password']
            amount              = data['amount']
            description         = data['description']
            counterparty        = data['counterparty']
            transaction_type_id = data['transaction_type_id']

            hashed_account_number = bcrypt.hashpw(account_number.encode('utf-8'), bcrypt.gensalt())
            print(hashed_account_number)
            # hash_account_number = bcrypt.checkpw(account_number.encode('utf-8'))
            account = Account.objects.get(user=user, account_number=account_number)

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
                        amount              = amount,
                        description         = description,
                        counterparty        = counterparty,
                        account_id          = account.id,
                        transaction_type_id = 1
                    )
                    account.balance = account.balance + amount
                    account.save()

                # transaction_type이 2일경우 출금
                elif transaction_type_id == 2:
                    if account.balance - amount < 0:
                        return JsonResponse({'message': 'INSUFFICIENT_IS_AMOUNT.'})
                    Transaction.objects.create(
                        amount              = amount,
                        description         = description,
                        counterparty        = counterparty,
                        account_id          = account.id,
                        transaction_type_id = 2
                    )
                    account.balance = account.balance - amount
                    account.save()

                return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)






