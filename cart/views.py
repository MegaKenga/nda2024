from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Offer
from cart.cart import Cart
from cart.forms import CartAddProductForm


@require_POST
def cart_add(request, offer_id):
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(offer=offer,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, offer_id):
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    cart.remove(offer)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/detail.html', {'cart': cart})
