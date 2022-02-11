from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mainapp.mixins import TitleContextMixin, SelfOrderAccessOnlyMixin
from mainapp.models import Product
from orderapp.forms import OrderForm, OrderItemForm
from orderapp.models import Order, OrderItem


class OrderListView(LoginRequiredMixin, TitleContextMixin, ListView):
    """Контроллер списка заказов пользователя"""
    model = Order
    title = 'Geekshop | Список заказов'

    def get_queryset(self):
        return self.request.user.order.filter(is_active=True)


class OrderCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = Order
    title = 'Geekshop | Создание заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orderapp:list')

    def get_context_data(self, **kwargs):  # ToDo - Переписать через миксин (повтор в OrderUpdateView)
        context = super().get_context_data(**kwargs)
        order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = order_form_set(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all()
            if basket_items:
                order_form_set = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = order_form_set()
                for basket, form in zip(basket_items, formset.forms):
                    form.initial['product'] = basket.product
                    form.initial['quantity'] = basket.quantity
                    form.initial['price'] = basket.product.price
            else:
                formset = order_form_set()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()  # Удаление корзин пользователя

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderDetailView(SelfOrderAccessOnlyMixin, TitleContextMixin, DetailView):
    """Контроллер с информацией о заказе"""
    model = Order
    title = 'Geekshop | Просмотр заказа'


class OrderUpdateView(SelfOrderAccessOnlyMixin, TitleContextMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orderapp:list')
    title = 'Geekshop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form_set = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = order_form_set(self.request.POST, instance=self.object)
        else:
            formset = order_form_set(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(SelfOrderAccessOnlyMixin, TitleContextMixin, DeleteView):
    """Контроллер удаления неоформленного заказа"""
    model = Order
    success_url = reverse_lazy('orderapp:list')
    title = 'Geekshop | Удаление заказа'


def to_order(request, pk):
    """Контроллер оформления заказа"""
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orderapp:list'))


def product_change(request, pk):
    """Контроллер модификации товара в заказе"""
    if request.accepts('text/html'):
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({'productPrice': product.price})
        except Exception as e:
            return JsonResponse({'error': str(e)})
