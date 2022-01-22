"""mainapp namespace url configuration"""

from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'
urlpatterns = [
    path('', mainapp.IndexTemplateView.as_view(), name='index'),
    path('products/', mainapp.ProductsListView.as_view(), name='products'),
    path('products/category/<slug:category_slug>/', mainapp.ProductsListView.as_view(), name='category'),
    path('product/<int:pk>/info/', mainapp.ProductInfoDetailView.as_view(), name='product_info')
]
