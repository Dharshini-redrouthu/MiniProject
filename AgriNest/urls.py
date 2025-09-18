# AgriNest/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('surplus/', include('surplus.urls', namespace='surplus')),
    path('stories/', include('stories.urls', namespace='stories')),
    path('support/', include('support.urls', namespace='support')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('notifications/', TemplateView.as_view(template_name='pages/notifications.html'), name='notifications'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='root_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
