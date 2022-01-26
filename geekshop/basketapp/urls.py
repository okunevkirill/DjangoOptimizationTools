"""basketapp namespace url configuration"""

from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'
urlpatterns = [
    path('add/<int:pk>/', basketapp.basket_add, name='basket_add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='basket_remove'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='basket_edit'),
]
