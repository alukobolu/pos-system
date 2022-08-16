from decimal import Decimal
from django.conf import settings

from .models import Inventory

# class  FinalPrice:
#     def __init__(self,price,method):
#         if method != "cash":
#             self.__final_price = price + 50
#         else:
#             self.__final_price = price

#     def get_final_price(self):
#         return self.__final_price

#     def __calculate_discount(self,discount):
#         return self.__final_price*(discount/100)

#     def set_final_price(self,discount):
#         self.__final_price = self.__final_price - self.__calculate_discount(discount)

        
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.__final_price = 0

    def add(self, product, quantity=1, price=None,method='', update_quantity=False):
        product_id = str(product.id)
        print(price)
        if price == None:
            price = product.sales_price
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

    def __calculate_discount(self,discount):
        return self.__final_price*(Decimal(discount)/100)

    def set_final_price(self,discount):
        self.__final_price = self.get_total_price()
        self.__final_price = self.__final_price - Decimal(self.__calculate_discount(discount))

    def get_final_price(self):
        return self.__final_price

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
