
from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eight_percent.settings")

from random import randint
from faker import Faker
from django_seed import Seed
import django
django.setup()

from users.models import Users
from transaction.models import Account, Transaction,TransactionType
from tqdm import tqdm
from random import randrange
import datetime
from django.utils import timezone

# datetime.datetime.now(tz=timezone.utc)



application = get_wsgi_application()


def dummy():
    for i in tqdm(range(100)):
        Account.objects.create(number=randint(1, 346723434234),
                               password="adfadf",
                               balance=randint(1000, 999999),
                               user=Users(1))

    for i in tqdm(range(100000)):
        start_date = datetime.datetime(2013, 9, 20, 13, 00, tzinfo=timezone.utc)
        end_date = datetime.datetime(2021, 2, 1, tzinfo=timezone.utc)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        Transaction.objects.create(
            amount=randint(1, 100),
            created_at=random_date,
            description="설명",
            counterparty="수신,발신",
            account=Account(randint(1, 100)),
            transaction_type=TransactionType(randint(1, 2))
        )


if __name__ == "__main__":
    dummy()
