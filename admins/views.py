from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryUpdateFormAdmin, ProductsForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, AdministratorAccessOnlyMixin, StaffAccessOnlyMixin
from mainapp.models import Product, ProductCategory
from ordersapp.models import Order


# -------------------------------------------------------------------------------
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


# -------------------------------------------------------------------------------
class OrderAdminListView(AdministratorAccessOnlyMixin, BaseClassContextMixin, ListView):
    model = Order
    template_name = 'admins/admin-order_list.html'
    title = 'Админка | Список заказов'


class OrderAdminDeleteView(AdministratorAccessOnlyMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('admins:orders')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def order_edit(request, id_order, status):
    if request.is_ajax():
        order = get_object_or_404(Order, id=id_order)
        if status != Order.CANCEL:
            order.status = status
            order.save()
        else:
            order.delete()

        orders = Order.objects.all()
        context = {'object_list': orders}
        result = render_to_string('admins/includes/table_orders.html', context)
        test = JsonResponse({'result': result})
        return test
