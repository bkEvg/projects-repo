from django.contrib import admin
from .models import Product, ProductSet, SizeSet, Size, Color


class SizeInline(admin.TabularInline):
	model = Size
	fk_name = 'size_set'


class SizeSetAdmin(admin.ModelAdmin):
	inlines = [SizeInline]
admin.site.register(SizeSet, SizeSetAdmin)


class ProductSetInline(admin.TabularInline):
	model = ProductSet
	fk_name = 'product'


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'stock', 'discount']
	inlines = [ProductSetInline]
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
