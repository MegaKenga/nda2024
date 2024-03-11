from .cart import Cart


def cart(request):
    cart_items_count = Cart(request).items_count()
    return {'cart_items_count': cart_items_count}
