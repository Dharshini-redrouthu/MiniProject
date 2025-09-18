from django.urls import path
from . import views

app_name = 'stories'
urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('<int:pk>/', views.story_detail, name='story_detail'),
]
