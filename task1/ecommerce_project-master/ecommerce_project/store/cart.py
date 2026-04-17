# store/cart.py
from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}
        if override:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        pids    = self.cart.keys()
        products = Product.objects.filter(id__in=pids)
        cart     = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price']    = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            yield item

    @property
    def total(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )