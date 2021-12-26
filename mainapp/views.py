from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView

from mainapp.mixin import BaseClassContextMixin
from mainapp.models import Product, ProductCategory


class MainIndexTemplateView(BaseClassContextMixin, TemplateView):
    """Site home page controller"""
    template_name = 'mainapp/index.html'
    title = 'Geekshop'


def products(request, id_category='0', page=1):  # ToDO Ok_kir - Переделать шаблон и контроллер под CBV
    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category != '0':
        products_active = Product.objects.filter(
            is_active=True, category__is_active=True).filter(category_id=id_category).order_by('id')
        category = get_object_or_404(ProductCategory, id=id_category)
    else:
        category = dict(pk=id_category, name='все')
        products_active = Product.objects.filter(is_active=True, category__is_active=True).order_by('id')

    paginator = Paginator(products_active, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['object_list'] = products_paginator
    context['current_category'] = category
    context['categories'] = ProductCategory.objects.filter(is_active=True)
    return render(request, 'mainapp/products.html', context)


# class MainProductsList(ListView):
#     template_name = 'mainapp/products.html'
#     model = Product
#     paginate_by = 3
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Geekshop'
#         context['current_category'] = self.kwargs.get('id_category', '0')
#         context['categories'] = ProductCategory.objects.filter(is_active=True)
#         return context
#

class ProductDetails(BaseClassContextMixin, DetailView):
    """Product information controller"""
    model = Product
    template_name = 'mainapp/detail.html'
    title = 'Информация о товаре'
