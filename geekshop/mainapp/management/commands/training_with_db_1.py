from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q

from orderapp.models import Order


class Command(BaseCommand):
    help = 'Script for working with Q model'

    def handle(self, *args, **options):
        """
        Функция вывода всех заказов не обновляющихся несколько дней и
        находящихся на выполнении"""
        obsolescence_time = now() - timedelta(hours=48)
        orders = Order.objects.filter(
            Q(updated__lt=obsolescence_time) |
            (~Q(status=Order.FORMING) & ~Q(status=Order.CANCEL))
        )

        print(orders)
