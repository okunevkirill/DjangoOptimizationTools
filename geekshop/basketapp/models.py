from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from mainapp.mixins import ProductQuantityMixin
from mainapp.models import Product


class Basket(ProductQuantityMixin, models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='basket',
                             verbose_name='ПОЛЬЗОВАТЕЛЬ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='ТОВАР')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='КОЛИЧЕСТВО')
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='ДОБАВЛЕНО')
    update_timestamp = models.DateTimeField(auto_now=True, verbose_name='ОБНОВЛЕНО')

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    class Meta:
        verbose_name_plural = f'Заказы пользователей'
        verbose_name = 'Заказ'

    @cached_property
    def get_items_cashed(self):
        return self.user.basket.select_related('product').all()

    def total_product_cost(self):
        return self.product.price * self.quantity

    def total_sum(self):  # ToDo - Возможно перенести функционал этого и след. метода в модель пользователя
        baskets = self.get_items_cashed
        return sum(basket.total_product_cost() for basket in baskets)

    def total_quantity(self):
        baskets = self.get_items_cashed
        return sum(basket.quantity for basket in baskets)
