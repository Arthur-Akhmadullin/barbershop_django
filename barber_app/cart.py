from decimal import Decimal
from django.conf import settings
from .models import Goods, Categories, GoodGroups

class Cart(object):
	def __init__(self, request):		
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:		
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		
	def add(self, good, quantity=1, update_quantity=False):		
		good_id = str(good.id)
		if good_id not in self.cart:
			self.cart[good_id] = {'quantity': 0, 'price': str(good.price)}
		if update_quantity:
			self.cart[good_id]['quantity'] = quantity
		else:
			self.cart[good_id]['quantity'] += quantity
		self.save()
		
	def save(self):
		#Этой строки не было в книге, но была на сайте pocoz.gitbooks.io
		#self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True
		
	def remove(self, good):		
		good_id = str(good.id)
		if good_id in self.cart:
			del self.cart[good_id]
			self.save()
			
	def __iter__(self):		
		good_ids = self.cart.keys()		
		goods = Goods.objects.filter(id__in=good_ids)
		cart = self.cart.copy()
		for good in goods:
			cart[str(good.id)]['good'] = good
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item
		
	def __len__(self):		
		return sum(item['quantity'] for item in self.cart.values())
		
	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
		
	def clear(self):		
		del self.session[settings.CART_SESSION_ID]
		self.save()