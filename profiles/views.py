from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        Profile.objects.create(user=user)
        
        return JsonResponse({'status': 'OK'})
    return render(request, 'profiles/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.all().filter(email = email).first()
        
        if user:
            if check_password(password, user.password):
                auth_login(request, user)
                return JsonResponse({ 'status': 'OK' })

            return JsonResponse({
                'status': 'KO',
                'msg': 'Either Your Email Or Password Is Incorrect'
            })
        
        return JsonResponse({
            'status': 'KO',
            'msg': 'Either Your Email Or Password Is Incorrect'
        })

    print(request.user.is_authenticated)

    return render(request, 'profiles/login.html')

def logout(request):
    auth_logout(request)
    return redirect("profiles:login")

@login_required
def success_page(request):
    print(request.user)
    return render(request, 'profiles/success.html')