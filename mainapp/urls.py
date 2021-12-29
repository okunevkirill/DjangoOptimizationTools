"""mainapp namespace url configuration"""

from django.urls import re_path
import mainapp.views as mainapp

app_name = 'mainapp'
urlpatterns = [
    re_path(r'^$', mainapp.MainIndexTemplateView.as_view(), name='index'),

    re_path(r'^products/$', mainapp.products, name='products'),
    # re_path(r'^products/category/(?P<id_category>\d+)/$', mainapp.MainProductsList.as_view(), name='category'),
    re_path(r'^products/category/(?P<id_category>\d+)/$', mainapp.products, name='category'),
    re_path(r'^products/category/(?P<id_category>\d+)/(?P<page>\d+)/$', mainapp.products, name='page'),

    re_path(r'^product/(?P<pk>\d+)/details/$', mainapp.ProductDetails.as_view(), name='details'),
]
