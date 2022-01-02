from django.contrib import admin

from ordersapp.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = (OrderItemAdmin,)
