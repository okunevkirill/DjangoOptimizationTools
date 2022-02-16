from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestUri(TestCase):
    """Класс тестирования основных uri путей приложения mainapp"""

    @classmethod
    def setUpClass(cls):
        category = ProductCategory.objects.create(name='test_1', slug='test1')
        Product.objects.create(category=category, name='product_1', price=100)
        Product.objects.create(category=category, name='product_2', price=100)
        cls.client = Client()

    def test_index(self):
        response = self.client.get(r'/')
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        response = self.client.get(r'/products/')
        self.assertEqual(response.status_code, 200)

    def test_product_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(fr'/product/{product_item.pk}/info/')
            self.assertEqual(response.status_code, 200)

    def test_products_by_category(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(fr'/products/category/{category.slug}/')
            self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        pass


class TestModels(TestCase):
    """Класс тестирования методов моделей"""

    def setUp(self):
        category = ProductCategory.objects.create(name='test_1', slug='test1')
        self.product_1 = Product.objects.create(
            name='Товар 1',
            description='Text 1',
            category=category,
            price=11.11,
            quantity=100,
            is_active=True,
        )
        self.product_2 = Product.objects.create(
            name='Товар 2',
            description='Text 2',
            category=category,
            price=200.00,
            quantity=50,
            is_active=True,
        )
        self.product_3 = Product.objects.create(
            name='Товар 3',
            description='Text 3',
            category=category,
            price=1000,
            quantity=500,
            is_active=False,
        )

    def test_print(self):
        self.assertEqual(str(self.product_1.category), 'test_1')
        self.assertEqual(str(self.product_1), 'Товар 1 | test_1')

    def test_get_absolute_url(self):
        self.assertEqual(self.product_2.get_absolute_url(), fr'/product/{self.product_2.pk}/info/')
