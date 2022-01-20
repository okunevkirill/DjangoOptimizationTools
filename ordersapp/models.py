from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    SEND_TO_PROCEED = 'S'
    PAID = 'P'
    PROCEEDED = 'W'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен в отработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order')
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлён', auto_now=True)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=1, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    class Meta:
        verbose_name_plural = 'заказы'
        verbose_name = 'заказ'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ № {self.id}'

    def get_all_products(self):
        return self.orderitem.select_related('product')

    def get_total_quantity(self):
        items = self.get_all_products()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.get_all_products()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    # def delete(self, using=None, keep_parents=False):
    #     for item in self.orderitem.select_related('product'):
    #         item.product.quantity += item.quantity
    #         item.save()
    #     self.is_active = False
    #     self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
