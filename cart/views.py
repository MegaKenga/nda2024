from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages


from catalog.models import Offer
from cart.forms import CartAddProductForm
from nda_email.forms import ContactForm
from django.views.generic import TemplateView
from nda_email.email_sender import EmailSender


CART_SESSION_ID = 'cart'


def get_cart(request):
    # session = request.session
    cart = request.session.get(CART_SESSION_ID)
    if not cart:
        # Сохраняем пустую корзину в сессии
        cart = request.session[CART_SESSION_ID] = {}
    return cart


def save_cart(request):
    cart = get_cart(request)
    # Обновление сессии cart/0
    request.session[CART_SESSION_ID] = cart
    # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
    request.session.modified = True
    return cart


def items_count(request):
    cart = get_cart(request)
    return len(cart.keys())


@require_POST
def cart_add(request, offer_id):
    cart = get_cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    item_add_form = CartAddProductForm(request.POST)
    if not item_add_form.is_valid():
        raise ValidationError('Invalid form')
    item_add_form_data = item_add_form.cleaned_data
    offer_id = str(offer.id)
    if offer_id not in cart:
        cart[offer_id] = {'quantity': item_add_form_data['quantity']}
    else:
        cart[offer_id]['quantity'] += item_add_form_data['quantity']
    save_cart(request)
    return redirect('offer', brand_slug=offer.category.brand.slug, category_slug=offer.category.slug)


def cart_remove(request, offer_id):
    cart = get_cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    offer_id = str(offer.id)
    if offer_id in cart:
        del cart[offer_id]
    save_cart(request)
    return redirect('cart_detail')


def cart_clear(request):
    # удаление корзины из сессии
    del request.session[CART_SESSION_ID]
    request.session.modified = True
    return redirect('cart_detail')


def get_cart_offers(request):
    cart = get_cart(request)
    offers = Offer.visible.filter(id__in=cart.keys())
    for offer in offers:
        offer_id = str(offer.id)
        offer_cart_record = cart.get(offer_id, None)
        if offer_cart_record is None:
            offer.quantity = 0
            print("offer_cart_record is None, which was not expected. Fallback to 0")
            continue
        offer.quantity = offer_cart_record.get('quantity', 0)
    return offers


def cart_detail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if not form.is_valid():
            return render(request,
                          'cart/detail.html',
                          {'offers': get_cart_offers(request), 'form': form})
        offers = get_cart_offers(request)
        EmailSender.send_submitted_order_and_customer_reply(request, offers)
        cart_clear(request)
        messages.success(request, 'Запрос успешно отправлен')
        return redirect('home')
    form = ContactForm()
    offers = get_cart_offers(request)
    return render(request, 'cart/detail.html', {'offers': offers, 'form': form})


class ContactSuccessView(TemplateView):
    template_name = 'cart/message_success.html'
