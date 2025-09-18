from django.shortcuts import render
from .models import SurplusItem

def surplus_list(request):
    items = SurplusItem.objects.all()
    return render(request, 'surplus/surplus_list.html', {'items': items})
