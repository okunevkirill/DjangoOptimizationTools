"""orders namespace url configuration"""

from django.urls import re_path
import ordersapp.views as ordersapp

app_name = 'ordersapp'
urlpatterns = [
    re_path(r'^$', ordersapp.OrderListView.as_view(), name='list'),
    re_path(r'^create/$', ordersapp.OrderCreateView.as_view(), name='create'),
    re_path(r'^read/(?P<pk>\d+)/$', ordersapp.OrderDetailView.as_view(), name='read'),
    re_path(r'^update/(?P<pk>\d+)/$', ordersapp.OrderUpdateView.as_view(), name='update'),
    re_path(r'^delete/(?P<pk>\d+)/$', ordersapp.OrderDeleteView.as_view(), name='delete'),

    re_path(r'^complete/(?P<pk>\d+)/$', ordersapp.complete, name='complete'),

]
