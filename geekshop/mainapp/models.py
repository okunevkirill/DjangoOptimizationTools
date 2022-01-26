from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='КАТЕГОРИЯ')
    slug = models.SlugField(max_length=64, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='ОПИСАНИЕ')
    is_active = models.BooleanField(default=True, verbose_name='АКТИВЕН')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'КАТЕГОРИИ'
        verbose_name = 'КАТЕГОРИЯ'
        ordering = ('slug', 'id')


class Product(models.Model):
    name = models.CharField(max_length=128, db_index=True, verbose_name='ТОВАР')
    image = models.ImageField(upload_to='product_image', blank=True, verbose_name='ИЗОБРАЖЕНИЕ')
    description = models.TextField(blank=True, null=True, verbose_name='ОПИСАНИЕ')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='ЦЕНА')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='КОЛИЧЕСТВО')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='КАТЕГОРИЯ')
    is_active = models.BooleanField(default=True, verbose_name='АКТИВЕН')

    def __str__(self):
        return f'{self.name} | {self.category}'

    class Meta:
        verbose_name_plural = 'ТОВАРЫ'
        verbose_name = 'ТОВАР'
        ordering = ('id',)

    def get_absolute_url(self):
        return reverse('mainapp:product_info', kwargs={'pk': self.pk})

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
