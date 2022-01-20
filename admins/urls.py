"""admins namespace url configuration"""

from django.urls import re_path
from django.views.i18n import set_language

import admins.views as admins

app_name = 'admins'
urlpatterns = [
    re_path(r'^$', admins.IndexTemplateView.as_view(), name='index'),
    re_path(r'^users/$', admins.UserListView.as_view(), name='admin_users'),
    re_path(r'^users-create/$', admins.UserCreateView.as_view(), name='admin_users_create'),
    re_path(r'^users-update/(?P<pk>\d+)/$', admins.UserUpdateView.as_view(), name='admin_users_update'),
    re_path(r'^users-delete/(?P<pk>\d+)/$', admins.UserDeleteView.as_view(), name='admin_users_delete'),

    re_path(r'^category/$', admins.CategoryListView.as_view(), name='admin_category'),
    re_path(r'^category/create/$', admins.CategoryCreateView.as_view(), name='admin_category_create'),
    re_path(r'^category-delete/(?P<pk>\d+)/$', admins.CategoryDeleteView.as_view(), name='admin_category_delete'),
    re_path(r'^category-update/(?P<pk>\d+)/$', admins.CategoryUpdateView.as_view(), name='admin_category_update'),
    # path('category-detail/<int:pk>/', admins.CategoryDetailView.as_view(), name='admin_category_detail'),

    re_path(r'^product/$', admins.ProductListView.as_view(), name='admins_product'),
    re_path(r'^products-update/(?P<pk>\d+)/$', admins.ProductsUpdateView.as_view(), name='admins_product_update'),
    re_path(r'^products-create/$', admins.ProductsCreateView.as_view(), name='admins_product_create'),
    re_path(r'^products-delete/(?P<pk>\d+)/$', admins.ProductsDeleteView.as_view(), name='admins_product_delete'),

    re_path(r'^lang/$', set_language, name='set_language'),

    re_path(r'^orders/$', admins.OrderAdminListView.as_view(), name='orders'),
    re_path(r'^orders/edit/(?P<id_order>\d+)/(?P<status>\w)/$', admins.order_edit, name='order_edit'),
    re_path(r'^orders/(?P<pk>\d+)/delete/$', admins.OrderAdminDeleteView.as_view(), name='order_delete'),
]
