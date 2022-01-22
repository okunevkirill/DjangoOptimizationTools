from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from basketapp.models import Basket
from orderapp.models import OrderItem


@transaction.atomic
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    quantity = instance.quantity    # ToDo - реализовать работу с quantity_stock через IntegrityError
    quantity_stock = instance.product.quantity
    if instance.pk:
        delta = quantity - instance.get_product_quantity(int(instance.pk))
    else:
        delta = quantity
    if delta > quantity_stock:
        delta = quantity_stock
    instance.product.quantity -= delta
    instance.product.save()


@transaction.atomic
@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
