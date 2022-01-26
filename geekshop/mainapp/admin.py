from django.contrib import admin

from mainapp.models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_active')
    fields = ('name', 'description', ('price', 'quantity'), 'category', 'image')
    ordering = ('name', 'price',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
