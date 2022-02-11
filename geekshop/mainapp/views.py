from django.views.generic import TemplateView, ListView, DetailView

from mainapp.mixins import TitleContextMixin
from mainapp.models import Product

from mainapp.mainapp_services import get_all_active_categories, get_category_by_slug, get_all_active_products


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
        context['categories'] = get_all_active_categories()
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_category_by_slug(category_slug)
            return Product.objects.select_related('category').filter(
                category=category, is_active=True, category__is_active=True)
        return get_all_active_products()


class ProductInfoDetailView(TitleContextMixin, DetailView):
    """Контроллер информации о продукте"""
    model = Product
    template_name = 'mainapp/product_info.html'
    title = 'Информация о товаре'
