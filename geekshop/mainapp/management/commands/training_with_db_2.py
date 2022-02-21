from django.core.management.base import BaseCommand
from prettytable import PrettyTable

from orderapp.models import OrderItem
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta

ACTION_1 = 1
ACTION_2 = 2
ACTION_EXPIRED = 3


class Command(BaseCommand):
    help = 'Script for working with the database at a low level'

    def handle(self, *args, **options):
        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = (
                Q(order__updated__gt=F('order__created') + action_1__time_delta) &
                Q(order__updated__lte=F('order__created') + action_2__time_delta)
        )

        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        table = PrettyTable(["Заказ", "Товар", "Скидка", 'Разница времени'])
        for order_item in test_orders:
            table.add_row(
                [f'{order_item.action_order} заказ №{order_item.pk:}',
                 f'{order_item.product.name:15}', f'{abs(order_item.total_price):6.2f} руб.',
                 order_item.order.updated - order_item.order.created]
            )
        print(table)
