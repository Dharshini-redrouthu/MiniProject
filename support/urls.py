from django.urls import path
from . import views
app_name = 'support' 
urlpatterns = [
    path('', views.pool_list, name='pool_list'),
]
