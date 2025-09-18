# AgriNest/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

ROLE_CHOICES = (
    ("farmer", "Farmer"),
    ("cooperative", "Cooperative"),
    ("retailer", "Retailer"),
    ("advisor", "Advisor"),
)

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    LANGUAGE_CHOICES = (("en", "English"), ("te", "Telugu"))
    language_pref = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="farmer")

    def __str__(self):
        return self.username or (self.mobile_number or "User")


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True)
    farm_size = models.CharField(max_length=100, blank=True, help_text="e.g. 2 acres")
    district = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.user}"


class OTPVerification(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.otp} - Verified: {self.is_verified}"
