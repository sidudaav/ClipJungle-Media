from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Profile, ProfileBlock, ProfileFollowRequest, ProfileFollowing
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .utils import get_user_by_email, get_user_by_username
from django.core.mail import EmailMessage


######################## AUUTHENTICATION VIEWS ########################
@require_POST
def register(request):
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if get_user_by_username(username):
        return JsonResponse({
            'status': 'KO',
            'errorField': 'Username',
            'msg': 'Username Is Taken'
        })

    if get_user_by_email(email):
        return JsonResponse({
            'status': 'KO',
            'errorField': 'Email',
            'msg': 'Email Is Taken'
        })
    
    ### NEED TO DO EMAIL VERIFICATION LATER ###
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = False
    user.save()

    email = EmailMessage(
        'Hello',
        'Body goes here',
        'from@example.com',
        [email],
    )

    email.send(fail_silently=False)

    Profile.objects.create(user=user)
    
    return JsonResponse({'status': 'OK'})

@require_POST
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    username = get_user_by_email(email)
    if username is None:
        return JsonResponse({
            'status': 'KO',
            'errorField': 'Email',
            'msg': 'Email Does Not Exist'
        })

    user = auth_authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return JsonResponse({
                'status': 'OK',
                'url': '/videos/home'
            })
        else:
            return JsonResponse({
                'status': 'KO',
                'errorField': 'Email',
                'msg': 'This Email Has Been Disabled'
            })
    else:
        pass
        return JsonResponse({
            'status': 'KO',
            'errorField': 'Password',
            'msg': 'Invalid Password'
        })

def logout(request):
    auth_logout(request)
    return redirect("profiles:auth")

def auth(request):
    if request.user.is_authenticated:
        return redirect("videos:home")
        
    return render(request, 'profiles/auth.html')


######################## PROFILE INTERACTION VIEWS ########################
@login_required
@require_POST
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
@require_POST
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
@require_POST
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