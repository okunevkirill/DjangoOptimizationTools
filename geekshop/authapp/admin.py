from django.contrib import admin

from authapp.models import User
from basketapp.admin import BasketAdmin
from basketapp.models import Basket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'first_name', 'last_name', 'email')
    model = Basket
    inlines = (BasketAdmin,)
    list_filter = ('date_joined',)
