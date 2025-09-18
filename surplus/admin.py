from django.contrib import admin
from .models import SurplusItem

@admin.register(SurplusItem)
class SurplusItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'discounted_price', 'status', 'seller')
    list_filter = ('status',)
