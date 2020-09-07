from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile

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
    return render(request, 'profiles/login.html')