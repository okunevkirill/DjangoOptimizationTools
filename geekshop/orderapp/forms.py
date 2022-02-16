from django import forms

# from mainapp.mainapp_services import get_all_active_products
from mainapp.models import Product
from orderapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'status', 'is_active')


class OrderItemForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=8, decimal_places=2, label='Цена', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['product'].queryset = get_all_active_products()
        self.fields['product'].queryset = Product.get_items()
