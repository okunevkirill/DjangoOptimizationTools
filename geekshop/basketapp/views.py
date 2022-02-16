from django.contrib.auth.decorators import login_required
# from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket_add(request, pk):
    """Контроллер добавления товара в корзину (работа через бд)"""
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    baskets = Basket.objects.filter(user=user, product=product)
    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        # basket.quantity = F('quantity') + 1
        basket.save()
    else:
        Basket.objects.create(user=user, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.accepts('text/html'):
        basket = get_object_or_404(Basket, pk=pk)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user).order_by(id)
        context = {'baskets': baskets}
        result_html = render_to_string('basketapp/inc__basket.html', context)
        return JsonResponse({'result': result_html})
