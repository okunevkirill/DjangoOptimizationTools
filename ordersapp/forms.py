from django import forms

from mainapp.mixin import CssFormattingMixin
from ordersapp.models import Order, OrderItem


class OrderForm(CssFormattingMixin, forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'status', 'is_active')


class OrderItemForm(CssFormattingMixin, forms.ModelForm):
    price = forms.DecimalField(max_digits=8, decimal_places=2, label='Цена', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'
