# AgriNest/accounts/urls.py
# AgriNest/accounts/urls.py
# AgriNest/accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    # Add this inside urlpatterns
    path('settings/', views.settings_view, name='settings'),

    # OTP verification
    path('verify-otp/<str:phone>/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/<str:phone>/', views.resend_otp_view, name='resend_otp'),
    # Add this inside urlpatterns
    path('logout/', views.logout_view, name='logout'),

    # Password reset (optional)
    # path('password-reset/', ...)
]


