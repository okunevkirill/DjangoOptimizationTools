from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from baskets.models import Basket
from mainapp.models import Product


@login_required
def basket_add(request, pk):
    user_select = request.user
    product = get_object_or_404(Product, id=pk)
    baskets = Basket.objects.filter(user=user_select, product=product)
    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id_basket):
    basket = get_object_or_404(Basket, id=id_basket)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id_basket, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = get_object_or_404(Basket, id=id_basket)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/basket.html', context)
        test = JsonResponse({'result': result})
        return test
