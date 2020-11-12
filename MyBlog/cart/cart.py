from django.conf import settings 
from shop.models import Product
from decimal import Decimal
from coupons.models import Coupon


class Cart(object):

	def __init__(self, request):
		"""
		Initialize cart
		"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		coupon_id = self.session.get(settings.COUPON_SESSION_ID)
		if not cart:
			#save na empty cart in the session
			cart = self.session[settings.CART_SESSION_ID]= {}
		self.cart = cart
		self.coupon_id = coupon_id

	def add(self, product, color, size=50, quantity=1, update_quantity=False):
		"""
		Add product or update quantity
		"""
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {
				'quantity': quantity,
				'price': str(product.price),
				'size': [size,],
				'color': [color,]
			}
		elif update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
			for i in range(quantity):
				self.cart[product_id]['size'].append(size)
				self.cart[product_id]['color'].append(color)
		self.save()

	def save(self):
		#refresh session of cart
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session[settings.COUPON_SESSION_ID] = self.coupon_id
		# mark session as modified for to be sure that session is saved
		self.session.modified = True

	def remove(self, product):
		"""
		Delete a product from a cart
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		"""
		Iter objects of product and getting products from db
		"""
		product_ids = self.cart.keys()
		#getting products and adding them to cart
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = float(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		"""
		Count all products in cart
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		"""
		Count price of all products in cart
		"""
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		"""
		delete cart from session
		"""
		del self.session[settings.CART_SESSION_ID]
		del self.session[settings.COUPON_SESSION_ID]	
		self.session.modified = True

	def clear_coupon(self):
		"""
		Delete a coupons from session
		"""
		del self.session[settings.COUPON_SESSION_ID]
		self.session.modified = True

	@property
	def coupon(self):
	    if self.coupon_id:
	        return Coupon.objects.get(id=self.coupon_id)
	    return None

	def get_discount(self):
	    if self.coupon:
	        return (self.coupon.discount / Decimal('100')) * self.get_total_price()
	    return Decimal('0')

	def get_total_price_after_discount(self):
	    return self.get_total_price() - self.get_discount()