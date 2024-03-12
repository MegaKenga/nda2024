from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Offer
from cart.cart import Cart
from cart.forms import CartAddProductForm, ContactForm
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy


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


def cart_remove(request, offer_id):
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    cart.remove(offer)
    return redirect('cart_detail')


def get_cart_offers(request):
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
    return offers


def cart_detail(request):
    offers = get_cart_offers(request)
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            return redirect('success')
    else:
        form = ContactForm()

    return render(request, 'cart/detail.html', {'offers': offers, 'form': form})


class ContactSuccessView(TemplateView):
    template_name = 'cart/success.html'
