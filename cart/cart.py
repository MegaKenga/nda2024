from django.conf import settings
from catalog.models import Offer


class Cart(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, offer, quantity=1):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        offer_id = str(offer.id)
        if offer_id not in self.cart:
            self.cart[offer_id] = {'quantity': 0}
        else:
            self.cart[offer_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart/0
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, offer):
        """
        Удаление товара из корзины.
        """
        offer_id = str(offer.id)
        if offer_id in self.cart:
            del self.cart[offer_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        offer_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        offers = Offer.objects.filter(id__in=offer_ids)
        for offer in offers:
            self.cart[str(offer.id)]['offer'] = offer

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
