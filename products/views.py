# AgriNest/products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home page - show all products
def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})

# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# Product details
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

# Add a product (only for logged-in users, e.g., farmers)
@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        Product.objects.create(
            name=name,
            slug=slug,
            description=description,
            price=price,
            category=category,
            owner=request.user
        )
        messages.success(request, 'Product added successfully!')
        return redirect('products:product_list')
    return render(request, 'products/add_product.html')

# List products by category
def products_by_category(request, category):
    products = Product.objects.filter(category__iexact=category)
    return render(request, 'products/product_list.html', {'products': products, 'category': category})
