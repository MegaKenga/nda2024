from cart.views import items_count


def cart(request):
    cart_items_count = items_count(request)
    return {'cart_items_count': cart_items_count}
