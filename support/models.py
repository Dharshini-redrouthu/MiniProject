### support/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class CropSupportPool(models.Model):
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_pools")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="pools", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Contribution(models.Model):
    pool = models.ForeignKey(CropSupportPool, on_delete=models.CASCADE, related_name="contributions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS = (("pending", "Pending"), ("completed", "Completed"), ("refunded", "Refunded"))
    status = models.CharField(max_length=20, choices=STATUS, default="completed")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == "completed":
            pool = self.pool
            pool.raised_amount = pool.contributions.filter(status="completed").aggregate(models.Sum('amount'))['amount__sum'] or 0
            pool.save()

    def __str__(self):
        return f"{self.amount} by {self.user} to {self.pool}"


