### surplus/models.py

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.conf import settings
from products.models import Product

class SurplusItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="surplus_items")
    quantity = models.PositiveIntegerField(default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    expiry_date = models.DateField(null=True, blank=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="surplus_sells")
    STATUS = (("active", "Active"), ("sold", "Sold"), ("removed", "Removed"))
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def is_near_expiry(self):
        if not self.expiry_date:
            return False
        return (self.expiry_date - timezone.now().date()).days <= 30

    def __str__(self):
        return f"Surplus: {self.product.name} ({self.quantity})"


