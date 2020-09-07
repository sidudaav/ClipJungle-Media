from django import forms
from .models import Video, VideoReport

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'allow_comments', 'tags', 'categories', 'video_file']

class VideoUpdateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'allow_comments', 'tags']

class VideoReportForm(forms.ModelForm):
    class Meta:
        model = VideoReport
        fields = ['choice_reason', 'written_reason']