from django.contrib import admin
from .models import CartItem, Order, OrderItem, Delivery

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
