from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.urls import reverse



class Product(models.Model):
	"""
	Product model
	"""
	name = models.CharField(max_length=200, db_index=True, verbose_name=u"Название")
	slug = models.SlugField(max_length=200, db_index=True, verbose_name=u"Артикул (лат.)", 
		help_text='То как этот товар будет отображен в URL.')
	description = models.TextField(default='Full description of product',blank=False, null=True, verbose_name=u"Описание",
		help_text='Добавьте полное описание товара, без характеристик.')
	short_description = models.CharField(default='Short description of product', max_length=100, verbose_name=u"Краткое описание", blank=False, null=True,
		help_text='Краткое описание, 3-4 слова.')
	product_composition = models.CharField(max_length=150, blank=False, null=True, verbose_name='Состав изделия')
	stock = models.PositiveIntegerField(default=1, verbose_name=u"В наличии (кол-во)")
	can_spend = models.BooleanField(default=False, verbose_name=u"Вычитать со склада")
	created = models.DateTimeField(auto_now_add=True, verbose_name=u"Создан")
	updated = models.DateTimeField(auto_now=True, verbose_name=u"Обновлен")
	### delete null=True out 'price_from'
	price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name=u"Цена от")
	discount = models.IntegerField(default=0, blank=True,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(100)],
                                                verbose_name='Скидка (%)')
	
	def __str__(self):
		return self.name

	class Meta:
		index_together = (('id','slug'),)
		verbose_name = 'товар'
		verbose_name_plural = 'товары'

	# def get_price(self):
	#     return Decimal(self.price - self.price * (self.discount / Decimal('100')))


	def get_absolute_url(self):
		return reverse('product__detail', args=[self.id, self.slug])



class SizeSet(models.Model):
	#product_item = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True)


	def __str__(self):
		return '{0}-{1}'.format(self.sizes.filter().first(), self.sizes.filter().last())


class Size(models.Model):
	size = models.CharField(max_length=4)
	size_set = models.ForeignKey(SizeSet, on_delete=models.CASCADE, related_name='sizes')

	def __str__(self):
		return self.size


class ProductSet(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sets')
	size_set = models.ForeignKey(SizeSet, on_delete=models.SET_NULL, null=True, related_name='size_set')
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name=u"Цена")
	slug = models.SlugField(max_length=200, unique=True, db_index=True)

	class Meta:
		verbose_name = 'сет товара'
		verbose_name_plural = 'сеты товаров'

	def __str__(self):
		return self.product.name


	def get_absolute_url(self):
		return reverse('product_set__detail', args=[self.product.id, self.product.slug, self.slug])




# class Color(models.Model):
# 	name = models.CharField('Цвет', default='', max_length=100)

# 	def __str__(self):
# 		return self.name

# 	class Meta:
# 		verbose_name = 'цвет'
# 		verbose_name_plural = 'цвета'
