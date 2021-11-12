from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eight_percent.settings")

from random import randint
from faker import Faker
from django_seed import Seed
import django

django.setup()

from users.models import Users
from transaction.models import Account, Transaction, TransactionType
from tqdm import tqdm
from random import randrange
import datetime
from django.utils import timezone


application = get_wsgi_application()



def dummy():
    for j in range(10):
        start_date = datetime.datetime(2000, 9, 20, 13, 00, tzinfo=timezone.utc)
        # id_front = int(start_date.strftime("%Y%m%d"))

        for i in tqdm(range(10000000)):
            start_date = start_date + datetime.timedelta(days=1)

            Transaction.objects.create(
                amount=100,
                created_at=start_date,
                description="설명",
                counterparty="수신,발신",
                balance= 300,
                account_id=randint(1,2),
                transaction_type_id= randint(1,2)
            )



if __name__ == "__main__":
    dummy()
