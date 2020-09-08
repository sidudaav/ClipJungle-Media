from django.shortcuts import render, get_object_or_404
from .models import Video, VideoReport
from profiles.models import ProfileFollowing
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

######################## JSON RESPONSE VIEWS ########################
@login_required
def like_video(request):
    video_id = request.POST.get('id')
    action = request.POST.get('action')

    if video_id and action:
        try:
            video = get_object_or_404(Video, id=video_id)
            if action == 'like':
                video.likes.add(request.user.profile)
            else:
                video.likes.remove(request.user.profile)

            return JsonResponse({ 'status': 'OK' })
        
        except:
            pass

    return JsonResponse({ 'status': 'KO'})


######################## VIDEO DISPLAY VIEWS ########################
@login_required
def home(request):
    profile = request.user.profile
    following_list = ProfileFollowing.objects.filter(profile_from=profile)

    def get_profile(obj):
        return obj.profile_to

    following_list = map(get_profile, following_list)

    video_list = Video.objects.filter(active=True, profile__user__is_active=True,
        profile__in=following_list).order_by('-created_on')
    
    return render(request, 'videos/home.html')