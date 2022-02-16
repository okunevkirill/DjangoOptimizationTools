"""adminapp namespace url configuration"""

from django.urls import path
from django.views.decorators.cache import cache_page

import adminapp.views as adminapp

app_name = 'adminapp'
urlpatterns = [
    path('', cache_page(3600)(adminapp.IndexTemplateView.as_view()), name='index'),
    path('users/', adminapp.UserListView.as_view(), name='users'),
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/', adminapp.CategoryListView.as_view(), name='categories'),
    path('category/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/', adminapp.ProductListView.as_view(), name='products'),
    path('product/create/', adminapp.ProductsCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', adminapp.ProductsDeleteView.as_view(), name='product_delete'),

    path('orders/', adminapp.OrderAdminappListView.as_view(), name='orders'),
    path('order/<int:pk>/delete/', adminapp.OrderAdminappDeleteView.as_view(), name='order_delete'),
    path('order/<int:id_order>/edit/<str:status>/', adminapp.order_edit, name='order_edit'),

]
