from cart.views import items_count, get_cart_offers
from nda_email.forms import ContactForm


def cart(request):
    cart_items_count = items_count(request)
    offers_in_cart = get_cart_offers(request)
    contact_form = ContactForm()
    return {'cart_items_count': cart_items_count, 'offers_in_cart': offers_in_cart, 'contact_form': contact_form}
