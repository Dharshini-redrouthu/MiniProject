from django.shortcuts import render
from .models import CropSupportPool

def pool_list(request):
    pools = CropSupportPool.objects.all()
    return render(request, 'support/pool_list.html', {'pools': pools})
