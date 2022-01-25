import json
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, file_name), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    """Management class for restoring the database"""

    help = 'Restore database from json'

    def handle(self, *args, **options):
        categories = load_from_json('categories.json')
        products = load_from_json('products.json')

        if not categories or not products:
            print('[!] Check the structure of the source data')
            return

        ProductCategory.objects.all().delete()
        Product.objects.all().delete()

        for category in categories:
            ProductCategory.objects.create(**category)

        for product in products:
            category_name = product['category']
            try:
                _category = ProductCategory.objects.get(name=category_name)
            except ObjectDoesNotExist:
                print(f'[!] {category_name} was not found')
                continue
            product['category'] = _category
            Product.objects.create(**product)
        print('[*] Database restored')
