from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(UserDispatchMixin, BaseClassContextMixin, ListView):
    model = Order
    title = 'Geekshop | Список заказов'

    def get_queryset(self):
        return self.request.user.order.filter(is_active=True)


class OrderCreateView(UserDispatchMixin, BaseClassContextMixin, CreateView):
    model = Order
    title = 'Geekshop | Создание заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all()
            if basket_items:
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for basket, form in zip(basket_items, formset.forms):
                    form.initial['product'] = basket.product
                    form.initial['quantity'] = basket.quantity
                    form.initial['price'] = basket.product.price
            else:
                formset = OrderFormSet()
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


class OrderDetailView(UserDispatchMixin, BaseClassContextMixin, DetailView):
    model = Order
    title = 'Geekshop | Просмотр заказа'


class OrderUpdateView(UserDispatchMixin, BaseClassContextMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
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


class OrderDeleteView(UserDispatchMixin, BaseClassContextMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Удаление заказа'


def complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))
