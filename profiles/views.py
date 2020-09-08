from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Profile, ProfileBlock, ProfileFollowRequest, ProfileFollowing
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.decorators import login_required

######################## BASIC HELPER FUNCTIONS ########################
def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

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
        return redirect("videos:home")

    return render(request, 'profiles/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username = get_user(email)
        user = auth_authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    'url': '/videos/home'
                })
            else:
                pass
                # Return a 'disabled account' error message
        else:
            pass
            # Return an 'invalid login' error message.

    print(request.user.is_authenticated)

    if request.user.is_authenticated:
        return redirect("videos:home")

    return render(request, 'profiles/login.html')

def logout(request):
    auth_logout(request)
    return redirect("profiles:login")


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

@login_required
def follow_profile(request):
    profile_id = request.POST.get('id')
    public = request.POST.get('public')
    action = request.POST.get('action')

    if profile_id and public and action:
        try:
            followed_profile = get_object_or_404(Profile, id=profile_id)
            if action == 'follow':
                if public == 'True':
                    ProfileFollowing.objects.get_or_create(profile_from=request.user.profile, profile_to=followed_profile)

                else:
                    ProfileFollowRequest.objects.get_object_or_404(profile_from=request.user.profile, profile_to=followed_profile)
            
            else:
                ProfileFollowing.objects.filter(profile_from=request.user.profile, profile_to=followed_profile).delete()
                ProfileFollowRequest.objects.filter(profile_from=request.user.profile, profile_to=followed_profile).delete()

            return JsonResponse({ 'status': 'OK' })
        
        except:
            pass
    
    return JsonResponse({ 'status': 'KO' })

@login_required
def modify_follow_request(request):
    profile_id = request.POST.get('id')
    action = request.POST.get('action')

    if profile_id and action:
        try:
            profile = get_object_or_404(Profile, id=profile_id)
            ProfileFollowRequest.objects.filter(user_from=profile, to=request.user.profile).delete()
            if action == 'accept':
                ProfileFollowRequest.objects.get_or_create(user_from=profile, to=request.user.profile)

            return JsonResponse({ 'status': 'OK' })
        
        except:
            pass
    
    return JsonResponse({ 'status': 'KO' })