import django.contrib.auth
from django.db import models
# from django.utils.functional import cached_property

from mainapp.mixins import ProductQuantityMixin
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    SEND_TO_PROCEED = 'S'
    PAID = 'P'
    PROCEEDED = 'W'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'ФОРМИРУЕТСЯ'),
        (SEND_TO_PROCEED, 'ОТПРАВЛЕН В ОТРАБОТКУ'),
        (PAID, 'ОПЛАЧЕН'),
        (PROCEEDED, 'ОБРАБАТЫВАЕТСЯ'),
        (READY, 'ГОТОВ К ВЫДАЧЕ'),
        (CANCEL, 'ОТМЕНЕН'),
    )

    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE, related_name='order')
    created = models.DateTimeField(verbose_name='СОЗДАН', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='ОБНОВЛЁН', auto_now=True)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES, verbose_name='СТАТУС', max_length=1, default=FORMING)
    is_active = models.BooleanField(verbose_name='АКТИВНЫЙ', default=True, db_index=True)

    class Meta:
        verbose_name_plural = 'ЗАКАЗЫ'
        verbose_name = 'ЗАКАЗ'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ № {self.id}'

    # @cached_property
    def get_all_products(self):
        return self.orderitems.select_related('product')

    def get_general_info(self):
        items = self.get_all_products()
        return {
            'total_quantity': sum(list(map(lambda x: x.quantity, items))),
            'total_cost': sum(list(map(lambda x: x.get_product_cost(), items)))
        }

    # def get_total_quantity(self):
    #     items = self.get_all_products
    #     return sum(list(map(lambda x: x.quantity, items)))
    #
    # def get_total_cost(self):
    #     items = self.get_all_products
    #     return sum(list(map(lambda x: x.get_product_cost(), items)))


class OrderItem(ProductQuantityMixin, models.Model):
    order = models.ForeignKey(Order, verbose_name='ЗАКАЗ', on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, verbose_name='ПРОДУКТЫ', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='КОЛИЧЕСТВО', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
