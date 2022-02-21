from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from adminapp.forms import UserAdminappCreationForm, UserAdminappChangeForm, ProductAdminappForm, CategoryAdminappForm
from mainapp.mixins import TitleContextMixin, AdminAccessOnlyMixin, StaffAccessOnlyMixin, \
    SpecializedRemovalDeleteViewMixin
from mainapp.models import ProductCategory, Product
from orderapp.models import Order


class IndexTemplateView(StaffAccessOnlyMixin, TitleContextMixin, TemplateView):
    """Контроллер основной страницы администрирования"""
    template_name = 'adminapp/admin.html'
    title = 'GeekShop - Admin'


# -------------------------------------------------------------------------------
class UserListView(AdminAccessOnlyMixin, TitleContextMixin, ListView):
    """Контроллер списка всех пользователей"""
    model = get_user_model()
    title = 'Админка | Пользователи'


class UserCreateView(AdminAccessOnlyMixin, TitleContextMixin, CreateView):
    """Контроллер создания нового пользователя"""
    model = get_user_model()
    template_name = 'adminapp/admin-user-create.html'
    form_class = UserAdminappCreationForm
    title = 'Админка | Создать пользователя'
    success_url = reverse_lazy('adminapp:users')


class UserUpdateView(AdminAccessOnlyMixin, TitleContextMixin, UpdateView):
    """Контроллер обновления информации о пользователе"""
    model = get_user_model()
    template_name = 'adminapp/admin-user-update-delete.html'
    form_class = UserAdminappChangeForm
    title = 'Админка | Обновить пользователя'
    success_url = reverse_lazy('adminapp:users')


class UserDeleteView(AdminAccessOnlyMixin, SpecializedRemovalDeleteViewMixin):
    """Контроллер удаления пользователя"""
    model = get_user_model()
    template_name = 'adminapp/admin-user-update-delete.html'
    form_class = UserAdminappChangeForm
    success_url = reverse_lazy('adminapp:users')


# -------------------------------------------------------------------------------
class CategoryListView(StaffAccessOnlyMixin, TitleContextMixin, ListView):
    model = ProductCategory
    title = 'Админка | Список категорий'


class CategoryCreateView(StaffAccessOnlyMixin, TitleContextMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-create.html'
    title = 'Админка | Создание категории'
    success_url = reverse_lazy('adminapp:categories')
    form_class = CategoryAdminappForm


class CategoryUpdateView(StaffAccessOnlyMixin, TitleContextMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-update-delete.html'
    form_class = CategoryAdminappForm
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('adminapp:categories')

    def form_valid(self, form):
        discount = form.cleaned_data.get('discount')
        if discount:
            self.object.product_set.update(
                price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(StaffAccessOnlyMixin, SpecializedRemovalDeleteViewMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('adminapp:categories')


# -------------------------------------------------------------------------------
class ProductListView(StaffAccessOnlyMixin, TitleContextMixin, ListView):
    model = Product
    title = 'Админка | Обновления категории'

    def get_queryset(self):
        return super().get_queryset().select_related('category')


class ProductsCreateView(StaffAccessOnlyMixin, TitleContextMixin, CreateView):
    model = Product
    template_name = 'adminapp/admin-product-create.html'
    form_class = ProductAdminappForm
    title = 'Админка | Создание продукта'
    success_url = reverse_lazy('adminapp:products')


class ProductUpdateView(StaffAccessOnlyMixin, TitleContextMixin, UpdateView):
    model = Product
    template_name = 'adminapp/admin-product-update-delete.html'
    form_class = ProductAdminappForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('adminapp:products')


class ProductsDeleteView(StaffAccessOnlyMixin, SpecializedRemovalDeleteViewMixin):
    model = Product
    template_name = 'mainapp/product_list.html'
    success_url = reverse_lazy('adminapp:products')


# -------------------------------------------------------------------------------
class OrderAdminappListView(AdminAccessOnlyMixin, TitleContextMixin, ListView):
    model = Order
    template_name = 'adminapp/admin-order_list.html'
    title = 'Админка | Список заказов'

    def get_queryset(self):
        return super().get_queryset().select_related()


class OrderAdminappDeleteView(AdminAccessOnlyMixin, SpecializedRemovalDeleteViewMixin):
    model = Order
    success_url = reverse_lazy('adminapp:orders')


@user_passes_test(lambda u: u.is_superuser)
def order_edit(request, id_order, status):
    if request.accepts('text/html'):
        order = get_object_or_404(Order, id=id_order)
        if status != Order.CANCEL:
            order.status = status
            order.save()
        else:
            order.delete()
        orders = Order.objects.all().order_by('pk')
        context = {'object_list': orders}
        result = render_to_string('adminapp/includes/inc__table_orders.html', context)
        result_response = JsonResponse({'result': result})
        return result_response
