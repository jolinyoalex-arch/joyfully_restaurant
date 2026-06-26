from decimal import Decimal
from django.conf import settings
from .models import MenuItem

class Cart:
    def _init_(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, chakula, quantity=1, override_quantity=False):
        chakula_id = str(chakula.id)
        if chakula_id not in self.cart:
            self.cart[chakula_id] = {'quantity': 0, 'price': str(chakula.bei)}
        
        if override_quantity:
            self.cart[chakula_id]['quantity'] = quantity
        else:
            self.cart[chakula_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, chakula):
        chakula_id = str(chakula.id)
        if chakula_id in self.cart:
            del self.cart[chakula_id]
            self.save()

    def _iter_(self):
        chakula_ids = self.cart.keys()
        vyakula = MenuItem.objects.filter(id__in=chakula_ids)
        cart = self.cart.copy()
        for chakula in vyakula:
            cart[str(chakula.id)]['chakula'] = chakula
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def _len_(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()