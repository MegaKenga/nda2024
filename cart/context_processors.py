from cart.views import get_cart_offers
from nda_email.forms import ContactForm, MailForm, CallForm, PhysicalContactForm


def cart(request):
    offers_in_cart = get_cart_offers(request)
    contact_form = ContactForm()
    mail_form = MailForm()
    call_form = CallForm()
    p_contact_form = PhysicalContactForm()
    return {
        'offers_in_cart': offers_in_cart, 'contact_form': contact_form, 'mail_form' : mail_form,
        'call_form' : call_form, 'p_contact_form': p_contact_form
    }
