from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST


from catalog.models import Offer
from cart.forms import CartAddProductForm
from nda_email.forms import ContactForm, PhysicalContactForm, MailForm, CallForm
from nda_email.email_sender import CompanyOrderEmailSender, PhysicalPersonOrderSender, CallRequestFormEmailSender, MailRequestFormEmailSender


CART_SESSION_ID = 'cart'

def get_cart(request):
    # Создаем корзину для сессии
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
        cart[offer_id]['quantity'] = item_add_form_data['quantity']
    save_cart(request)
    return render(request, 'cart/cart.html')


def cart_remove(request, offer_id):
    cart = get_cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    offer_id = str(offer.id)
    if offer_id in cart:
        del cart[offer_id]
    save_cart(request)
    return render(request, 'cart/cart_popup.html')


def cart_clear(request):
    if request.session.get(CART_SESSION_ID):
        del request.session[CART_SESSION_ID]
        request.session.modified = True


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


def cart_modal(request):
    form = ContactForm()
    offers = get_cart_offers(request)
    return render(request, 'cart/cart_modal.html', {'offers': offers, 'form': form})

@require_POST
def cart_submit(request):
    captcha_response = validate_captcha(request)
    captcha_valid = captcha_response is True

    form = ContactForm(request.POST, request.FILES)
    offers = get_cart_offers(request)
#     validate_captcha(request)
    return form_send_message(request, form, CompanyOrderEmailSender, offers=offers, captcha_valid=captcha_valid)


@require_POST
def physical_cart_submit(request):
    captcha_response = validate_captcha(request)
    captcha_valid = captcha_response is True

    form = PhysicalContactForm(request.POST, request.FILES)
    offers = get_cart_offers(request)
    return form_send_message(request, form, PhysicalPersonOrderSender, offers=offers, captcha_valid=captcha_valid)


@require_POST
def mail_submit(request):
    captcha_response = validate_captcha(request)
    # Если captcha_response == True → капча пройдена
    # Если captcha_response == HttpResponse → капча не пройдена
    captcha_valid = captcha_response is True

    form = MailForm(request.POST, request.FILES)
    return form_send_message(request, form, MailRequestFormEmailSender, offers=None, captcha_valid=captcha_valid)


@require_POST
def call_submit(request):
    form = CallForm(request.POST)
    if form.is_valid():
        try:
            CallRequestFormEmailSender.send_messages(request)
            # Возвращаем JSON для успешного ответа
            return JsonResponse({'success': True, 'message': 'Форма успешно отправлена'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'errors': 'Ошибка при отправке'}, status=500)
    else:
        # Возвращаем ошибки валидации
        errors = {field: error[0] for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)
