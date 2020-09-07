from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile, ProfileBlock, ProfileFollowRequest, ProfileFollowing
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

######################## AUUTHENTICATION VIEWS ########################
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
        
    if request.user.is_authenticated:
        return redirect("profiles:success-page")

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

    if request.user.is_authenticated:
        return redirect("profiles:success-page")

    return render(request, 'profiles/login.html')

def logout(request):
    auth_logout(request)
    return redirect("profiles:login")

@login_required
def success_page(request):
    print(request.user)
    return render(request, 'profiles/success.html')


######################## PROFILE INTERACTION VIEWS ########################
@login_required
def block_profile(request):
    profile_id = request.POST.get('id')
    action = request.POST.get('action')

    if profile_id and action:
        try:
            blocked_profile = get_object_or_404(Profile, id=profile_id)
            if action == 'block':
                ProfileBlock.objects.get_or_create(profile_from=request.user.profile, profile_to=blocked_profile)

                ProfileFollowRequest.objects.filter(profile_from=request.user.profile, profile_to=blocked_profile).delete()
                ProfileFollowRequest.objects.filter(profile_from=blocked_profile, profile_to=request.user.profile).delete()

                ProfileFollowing.objects.filter(profile_from=request.user.profile, profile_to=blocked_profile).delete()
                ProfileFollowing.objects.filter(profile_from=blocked_profile, profile_to=request.user.profile).delete()

            else:
                ProfileBlock.objects.filter(profile_from=request.user.profile, user_to=blocked_profile)
            
            return JsonResponse({ 'status': 'OK' })
        
        except:
            pass
    
    return JsonResponse({ 'status': 'KO' })