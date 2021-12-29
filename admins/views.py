from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryUpdateFormAdmin, ProductsForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, AdministratorAccessOnlyMixin, StaffAccessOnlyMixin
from mainapp.models import Product, ProductCategory


class IndexTemplateView(StaffAccessOnlyMixin, TemplateView):
    template_name = 'admins/admin.html'


# -------------------------------------------------------------------------------
class UserListView(AdministratorAccessOnlyMixin, ListView, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserCreateView(AdministratorAccessOnlyMixin, CreateView, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'


class UserUpdateView(AdministratorAccessOnlyMixin, UpdateView, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновить пользователя'


class UserDeleteView(AdministratorAccessOnlyMixin, DeleteView, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# -------------------------------------------------------------------------------
class CategoryListView(StaffAccessOnlyMixin, ListView, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    title = 'Админка | Список категорий'

    def get_queryset(self):
        if self.kwargs:
            return ProductCategory.objects.filter(id=self.kwargs.get('pk'))
        else:
            return ProductCategory.objects.all()


class CategoryDeleteView(StaffAccessOnlyMixin, DeleteView, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(StaffAccessOnlyMixin, UpdateView, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('admins:admin_category')


class CategoryCreateView(StaffAccessOnlyMixin, CreateView, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Создание категории'


# -------------------------------------------------------------------------------
class ProductListView(StaffAccessOnlyMixin, ListView, BaseClassContextMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    title = 'Админка | Обновления категории'


class ProductsUpdateView(StaffAccessOnlyMixin, UpdateView, BaseClassContextMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductsForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('admins:admins_product')


class ProductsCreateView(StaffAccessOnlyMixin, CreateView, BaseClassContextMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    form_class = ProductsForm
    title = 'Админка | Создание продукта'
    success_url = reverse_lazy('admins:admins_product')


class ProductsDeleteView(StaffAccessOnlyMixin, DeleteView):
    model = Product
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:admins_product')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
