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
        form_data = form.cleaned_data
        cart.add(offer=offer,
                 quantity=form_data['quantity']
                 )
    return redirect('cart_detail')


# @require_POST
# def cart_add_2(request, offer_id):
#     cart = request.session.get('cart', {})
#     if offer_id not in cart:
#         cart[offer_id] = 1
#     request.session['cart'] = cart
#     return redirect('cart_detail')
#
# def cart_detail_2(request):
#     cart = request.session.get('cart', {})
#     offers = Offer.visible.filter(id__in=cart.keys())
#     return render(request, 'cart/detail.html', {'offers': offers})

def cart_remove(request, offer_id):
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    cart.remove(offer)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request).cart
    offers = Offer.visible.filter(id__in=cart.keys())
    for offer in offers:
        offer_id = str(offer.id)
        offer_cart_record = cart.get(offer_id, None)
        if offer_cart_record is None:
            offer.quantity = 0
            print("offer_cart_record is None, which was not expected. Fallback to 0")
            continue
        offer_quantity = offer_cart_record.get('quantity', 0)
        offer.quantity = offer_quantity
    return render(request, 'cart/detail.html', {'offers': offers})
