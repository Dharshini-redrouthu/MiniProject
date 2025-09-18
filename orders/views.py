from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .models import CartItem, Order, OrderItem, Delivery
from products.models import Product
from django.contrib import messages

# List of orders for logged-in user
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

# Detail view of a single order
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'price_at_add_time': product.price, 'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('orders:order_list')

# Remove item from cart
@login_required
def remove_from_cart(request, order_id):
    cart_item = get_object_or_404(CartItem, id=order_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('orders:order_list')

# Checkout and create an order
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('orders:order_list')

    total = sum(item.line_total() for item in cart_items)
    order_number = get_random_string(length=12).upper()

    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        total_amount=total,
        shipping_address="Default address",  # Replace with actual user address
        status="PLACED",
        payment_status="PENDING"
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price_at_add_time
        )

    cart_items.delete()  # Clear cart after checkout
    messages.success(request, f"Order {order_number} placed successfully!")
    return redirect('orders:order_detail', pk=order.id)

# Show payment history for the user
@login_required
def payment_history(request):
    orders = Order.objects.filter(user=request.user).exclude(payment_status="PENDING")
    return render(request, 'orders/payment_history.html', {'orders': orders})
