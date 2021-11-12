import json

from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Account, Transaction, TransactionType


class TransactionHistoryView(View):
    def get(self, request):
        data = json.loads(request.body)
        account_number = data['account_number']
        transaction_type = data['transaction_type']
        start_date = data['start_date']
        end_date = data['end_date']

        transaction = Transaction.objects.filter(
            Q(account_id=account_number) & Q(transaction_type=transaction_type) & Q(
                created_at__range=[str(start_date), str(end_date)])).order_by('created_at')
        paginated_transaction = Paginator(transaction, 3).get_page(3)
        for i in paginated_transaction:
            print(i)
        print(paginated_transaction)
        return JsonResponse({'data': {'products': "mber", }}, status=200)
