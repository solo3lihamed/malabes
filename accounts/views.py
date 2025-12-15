from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            phone = request.POST.get('phone', '')
            UserProfile.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, f'مرحباً {user.username}! تم إنشاء حسابك بنجاح 🎉')
            return redirect('shop:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً بعودتك {username}! 👋')
                return redirect('shop:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """User logout"""
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح. نراك قريباً! 👋')
    return redirect('shop:home')


@login_required
def profile(request):
    """User profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.save()
        messages.success(request, 'تم تحديث معلوماتك بنجاح! ✅')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'profile': profile})
