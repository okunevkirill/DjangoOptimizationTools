"""orders namespace url configuration"""

from django.urls import path
import orderapp.views as orderapp

app_name = 'orderapp'
urlpatterns = [
    path('', orderapp.OrderListView.as_view(), name='list'),
    path('create/', orderapp.OrderCreateView.as_view(), name='create'),
    path('read/<int:pk>/', orderapp.OrderDetailView.as_view(), name='read'),
    path('update/<int:pk>/', orderapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', orderapp.OrderDeleteView.as_view(), name='delete'),

    path('complete/<int:pk>/', orderapp.to_order, name='to_order'),
    path('product/change/<int:pk>/', orderapp.product_change, name='product_change'),
]
