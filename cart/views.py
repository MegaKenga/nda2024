from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json
import logging
from catalog.models import Offer
from cart.forms import CartAddProductForm

from nda_email.forms import ContactForm, PhysicalContactForm, MailForm, CallForm
from nda_email.email_sender import LegalEntityEmailSender, PhysicalPersonEmailSender, MailFormEmailSender, CallFormEmailSender
from nda_email.captcha import get_client_ip, yandex_captcha_validation


CART_SESSION_ID = 'cart'
logger = logging.getLogger(__name__)

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


def cart_submit(request):
    form = ContactForm(request.POST, request.FILES)
    offers = get_cart_offers(request)
    if request.session.get('captcha_passed', False):
        pass 
    else:
        token = request.POST.get('smart-token')
        client_ip = get_client_ip(request)
        if not yandex_captcha_validation(token, client_ip):
            response = HttpResponse(status=400)
            response['HX-Trigger'] = json.dumps({"showError": "Докажите, что вы не робот", "reloadPage": True})
            return response
        else:
            request.session['captcha_passed'] = True
            request.session.set_expiry(600)  
    if form.is_valid():
        try:
            LegalEntityEmailSender().send_messages(request, offers)
            cart_clear(request)
            response = HttpResponse(status=200)
            response['HX-Trigger'] = json.dumps({"showMessage": "Запрос отправлен", "reloadPage": True})
            del request.session['captcha_passed']
            return response
        except Exception as e:
            logger.exception("Ошибка при отправке сообщения")
            response = HttpResponse(status=500)
            response['HX-Trigger'] = json.dumps({"showError": "Форма не отправлена"})
            return response
    else:
        errors = dict(form.errors.items())
        error_message = ""
        for field, messages in errors.items():
            error_message += f"{field}: {messages[0]}\n"

        response = HttpResponse(status=400)  
        response['HX-Trigger'] = json.dumps({
            "showError": error_message,
        })
        return response
    
@require_POST
def physical_cart_submit(request):
    form = PhysicalContactForm(request.POST, request.FILES) 
    offers = get_cart_offers(request)
    if request.session.get('captcha_passed', False):
        pass 
    else:
        token = request.POST.get('smart-token')
        client_ip = get_client_ip(request)
        if not yandex_captcha_validation(token, client_ip):
            response = HttpResponse(status=400)
            response['HX-Trigger'] = json.dumps({"showError": "Докажите, что вы не робот", "reloadPage": True})
            return response
        else:
            request.session['captcha_passed'] = True
            request.session.set_expiry(600)  
    if form.is_valid():
        try:
            PhysicalPersonEmailSender.send_messages(request, offers)
            cart_clear(request)
            response = HttpResponse(status=200)
            response['HX-Trigger'] = json.dumps({"showMessage": "Запрос отправлен", "reloadPage": True})
            del request.session['captcha_passed']
            return response
        except Exception as e:
            logger.exception("Ошибка при отправке сообщения")
            response = HttpResponse(status=500)
            response['HX-Trigger'] = json.dumps({"showError": "Форма не отправлена"})
            return response
    else:
        errors = dict(form.errors.items())
        error_message = ""
        for field, messages in errors.items():
            error_message += f"{field}: {messages[0]}\n"

        response = HttpResponse(status=400)  
        response['HX-Trigger'] = json.dumps({
            "showError": error_message,
        })
        return response

@require_POST
def mail_submit(request):
    form = MailForm(request.POST, request.FILES)
    if request.session.get('captcha_passed', False):
        pass  
    else:
        token = request.POST.get('smart-token')
        client_ip = get_client_ip(request)

        if not yandex_captcha_validation(token, client_ip):
            response = HttpResponse(status=400)
            response['HX-Trigger'] = json.dumps({"showError": "Докажите, что вы не робот", "reloadPage": True})
            return response
        else:
            request.session['captcha_passed'] = True
            request.session.set_expiry(600) 

    if form.is_valid():
        try:
            CallFormEmailSender.send_messages(request)
            response = HttpResponse(status=200)
            response['HX-Trigger'] = json.dumps({"showMessage": "Запрос отправлен", "reloadPage": True})
            del request.session['captcha_passed']
            return response
        except Exception as e:
            logger.exception("Ошибка при отправке сообщения")
            response = HttpResponse(status=500)
            response['HX-Trigger'] = json.dumps({"showError": "Форма не отправлена"})
            return response
    else:
        errors = dict(form.errors.items())
        error_message = ""
        for field, messages in errors.items():
            error_message += f"{field}: {messages[0]}\n"

        response = HttpResponse(status=400)  
        response['HX-Trigger'] = json.dumps({
            "showError": error_message,
        })
        return response

@require_POST
def call_submit(request):
    form = CallForm(request.POST, request.FILES)
    if request.session.get('captcha_passed', False):
        pass 
    else:
        token = request.POST.get('smart-token')
        client_ip = get_client_ip(request)

        if not yandex_captcha_validation(token, client_ip):
            response = HttpResponse(status=400)
            response['HX-Trigger'] = json.dumps({"showError": "Докажите, что вы не робот", "reloadPage": True})
            return response
        else:
            request.session['captcha_passed'] = True
            request.session.set_expiry(600) 

    if form.is_valid():
        try:
            CallFormEmailSender.send_messages(request)
            response = HttpResponse(status=200)
            response['HX-Trigger'] = json.dumps({"showMessage": "Запрос отправлен", "reloadPage": True})
            del request.session['captcha_passed']
            return response
        except Exception as e:
            logger.exception("Ошибка при отправке сообщения")
            response = HttpResponse(status=500)
            response['HX-Trigger'] = json.dumps({"showError": "Форма не отправлена"})
            return response
    else:
        errors = dict(form.errors.items())
        error_message = ""
        for field, messages in errors.items():
            error_message += f"{field}: {messages[0]}\n"

        response = HttpResponse(status=400)  
        response['HX-Trigger'] = json.dumps({
            "showError": error_message,
        })
        return response
        
