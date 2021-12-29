from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket', verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='время добавления')
    update_timestamp = models.DateTimeField(auto_now=True, verbose_name='время обновления')

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    class Meta:
        verbose_name_plural = f'Заказы пользователей'
        verbose_name = 'Заказ'

    def total_product_cost(self):
        return self.product.price * self.quantity

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.total_product_cost() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)
