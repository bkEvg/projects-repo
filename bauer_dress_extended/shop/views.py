from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSet, SizeSet
from .forms import CartAddProductForm

def list(request):
	products = Product.objects.all()
	return render(request, 'shop/list.html', {'products': products})

def product__detail(request, pk, slug):
	product = get_object_or_404(Product, pk=pk, slug=slug)
	return render(request, 'shop/detail.html', {'product': product})


def product_set__detail(request, pk, slug, set_slug):
	product = get_object_or_404(Product, pk=pk, slug=slug)
	set = get_object_or_404(ProductSet, slug=set_slug)
	size_set = get_object_or_404(SizeSet, size_set=set)
	form = CartAddProductForm()
	sets = product.sets.all().exclude(size_set=size_set)
	current_set = product.sets.get(size_set=size_set)
	return render(request, 'shop/detail_with_set.html', {'product': product,
														'set': set,
														'sets': sets,
														'current_set': current_set,
														'form': form})