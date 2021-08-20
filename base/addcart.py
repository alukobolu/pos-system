from decimal import Decimal
from django.conf import settings

from .models import Inventory


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, price=None,method='', update_quantity=False):
        product_id = str(product.id)
        print(price)
        if price == None:
            price = product.sales_price
        if method =="POS":
            price = int(price) + 50
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(price), 'method': method}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['price'] = price
            self.cart[product_id]['method'] = method
        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['price'] = price
            self.cart[product_id]['method'] = method
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Inventory.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['method'] = item['method']
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
