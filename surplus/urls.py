from django.urls import path
from . import views

app_name = 'surplus' 
urlpatterns = [
    path('', views.surplus_list, name='surplus_list'),
]
