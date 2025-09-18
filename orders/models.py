### orders/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from products.models import Product

ORDER_STATUS = (
    ("PLACED", "Placed"),
    ("PROCESSING", "Processing"),
    ("SHIPPED", "Shipped"),
    ("DELIVERED", "Delivered"),
    ("CANCELLED", "Cancelled"),
)
PAYMENT_STATUS = (("PENDING", "Pending"), ("SUCCESS", "Success"), ("FAILED", "Failed"))

class CartItem(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_add_time = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    def line_total(self):
        return self.quantity * self.price_at_add_time

    def __str__(self):
        return f"CartItem: {self.product.name} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    order_number = models.CharField(max_length=32, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PLACED")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product} x {self.quantity}"

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    tracking_code = models.CharField(max_length=80, blank=True, null=True)
    courier = models.CharField(max_length=120, blank=True, null=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PROCESSING")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for {self.order.order_number} - {self.status}"
