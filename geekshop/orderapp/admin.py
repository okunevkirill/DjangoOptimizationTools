from django.contrib import admin

from orderapp.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity')
    extra = 0
    verbose_name_plural = 'ТОВАРЫ'
    verbose_name = 'ТОВАР'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'user', 'status', 'created', 'updated', 'is_active')
    list_display_links = ('id', 'user', 'status')
    list_filter = ('status', 'created', 'updated', 'is_active')
    inlines = (OrderItemAdmin,)
