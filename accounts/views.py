import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from .models import CustomUser, OTPVerification
from .forms import SignUpForm, OTPForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until OTP verified
            user.save()
            
            # Generate OTP and save
            otp = str(random.randint(100000, 999999))
            OTPVerification.objects.create(phone_number=user.mobile_number, otp=otp)
            messages.success(request, f'OTP sent to {user.mobile_number}. (dev-only: {otp})')
            
            return redirect('accounts:verify_otp', phone=user.mobile_number)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def verify_otp_view(request, phone):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            otp_record = OTPVerification.objects.filter(
                phone_number=phone, otp=otp, is_verified=False
            ).first()
            
            if otp_record:
                # Activate user
                user = CustomUser.objects.get(mobile_number=phone)
                user.is_active = True
                user.is_mobile_verified = True
                user.save()
                
                # Mark OTP as verified
                otp_record.is_verified = True
                otp_record.save()
                
                login(request, user)
                messages.success(request, _('Account verified successfully!'))
                return redirect('products:home')
            else:
                messages.error(request, _('Invalid OTP'))
    else:
        form = OTPForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form, 'phone': phone})


def resend_otp_view(request, phone):
    otp_record = OTPVerification.objects.filter(phone_number=phone, is_verified=False).first()
    
    if otp_record:
        otp_record.otp = str(random.randint(100000, 999999))
        otp_record.save()
        messages.success(request, f'OTP resent to {phone}. (dev-only: {otp_record.otp})')
    else:
        messages.error(request, _('No pending OTP found for this number.'))
    
    return redirect('accounts:verify_otp', phone=phone)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('Logged out successfully.'))
    return redirect('accounts:login')


@login_required
def profile_view(request):
    orders = getattr(request.user, 'order_set', None)
    if orders:
        orders = orders.all()[:10]
    return render(request, 'accounts/profile.html', {'orders': orders})

@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')

