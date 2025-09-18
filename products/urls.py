# products/urls.py
from django.urls import path
from . import views

app_name = 'products'  # <--- required for namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('category/<str:category>/', views.products_by_category, name='products_by_category'),
]
