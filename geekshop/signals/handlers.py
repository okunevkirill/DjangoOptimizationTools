from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from django.db import connection

from basketapp.models import Basket
from mainapp.models import ProductCategory
from orderapp.models import OrderItem


def _db_profile_by_type(prefix, query_type, queries):
    """Функция иллюстрации sql запросов"""
    update_queries = list(filter(lambda x: query_type in x['sql'], queries))
    print(f'db_profile {query_type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@transaction.atomic
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    quantity = instance.quantity
    if instance.pk:
        delta = quantity - sender.get_item(pk=int(instance.pk))
    else:
        delta = quantity
    instance.product.quantity = F('quantity') - delta
    instance.product.save()
    if settings.DEBUG:
        _db_profile_by_type(instance.product, 'UPDATE', connection.queries)


@transaction.atomic
@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity = F('quantity') + instance.quantity
    instance.product.save()
    if settings.DEBUG:
        _db_profile_by_type(instance.product, 'UPDATE', connection.queries)


@transaction.atomic
@receiver(post_save, sender=ProductCategory)
def productcategory_is_active_update(sender, instance, **kwargs):
    """
    Сигнал формирования активности товара в зависимости от активности категории.
    [*] При восстановлении активности у категории все товары этой категории станут также активными
    """
    if instance.pk:
        instance.product_set.update(is_active=bool(instance.is_active))
