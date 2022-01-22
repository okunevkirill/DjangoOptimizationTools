# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.mixins import TitleContextMixin
from mainapp.models import Product, ProductCategory


class IndexTemplateView(TitleContextMixin, TemplateView):
    """Контроллер домашней страницы сайта"""
    template_name = 'mainapp/index.html'
    title = 'Geekshop'


class ProductsListView(TitleContextMixin, ListView):
    """Контроллер списка всех продуктов магазина"""
    template_name = 'mainapp/products.html'
    model = Product
    title = 'Geekshop | Каталог'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(ProductCategory, slug=category_slug)
            return Product.objects.filter(category=category, is_active=True, category__is_active=True)
        return Product.objects.filter(is_active=True).order_by('name')


class ProductInfoDetailView(TitleContextMixin, DetailView):
    """Контроллер информации о продукте"""
    model = Product
    template_name = 'mainapp/product_info.html'
    title = 'Информация о товаре'
