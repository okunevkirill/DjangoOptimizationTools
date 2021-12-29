"""baskets namespace url configuration"""

from django.urls import re_path
import baskets.views as baskets

app_name = 'baskets'
urlpatterns = [
    re_path(r'^add/(?P<pk>\d+)/$', baskets.basket_add, name='basket_add'),
    re_path(r'^remove/(?P<id_basket>\d+)/$', baskets.basket_remove, name='basket_remove'),
    re_path(r'^edit/(?P<id_basket>\d+)/(?P<quantity>\d+)/$', baskets.basket_edit, name='basket_edit'),
]
