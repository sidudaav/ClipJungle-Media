from django.shortcuts import render, get_object_or_404
from .models import Video, VideoReport
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