### products/models.py

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    image = models.ImageField(upload_to="category/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

SEASON_CHOICES = (
    ("kharif", "Kharif"),
    ("rabi", "Rabi"),
    ("zaid", "Zaid"),
)

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=120, unique=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=30, default="unit")
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    min_order_qty = models.PositiveIntegerField(default=1)
    is_wholesale = models.BooleanField(default=False)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    season_tag = models.CharField(max_length=20, choices=SEASON_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/images/")
    alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


