from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache

from mainapp.models import ProductCategory, Product


def get_all_active_categories():
    """Функция получения списка всех активных категорий (с возможностью кэширования)"""
    if settings.LOW_CACHE:
        key = 'active_categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.filter(is_active=True)
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category_by_slug(slug: str):
    """Функция получения категории по слагу (с возможностью кэширования)"""
    if settings.LOW_CACHE:
        key = f'category_by_slug_{slug}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, slug=slug)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, slug=slug)


def get_all_active_products():
    """Функция получения списка всех активных товаров (с возможностью кэширования)"""
    if settings.LOW_CACHE:
        key = 'active_products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.select_related('category').filter(is_active=True, category__is_active=True)
            cache.set(key, products)
        return products
    return Product.objects.select_related('category').filter(is_active=True, category__is_active=True)
