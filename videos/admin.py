from django.contrib import admin
from .models import Video, VideoReport

class VideoAdmin(admin.ModelAdmin):
    list_display = ['profile', 'id', 'title', 'slug', 'category', 'hot_score', 'created_on', 'active']
    list_filter = ['created_on']
    search_fields = ['profile', 'title', 'category__title']
    actions = ['approve_videos', 'block_videos']

    def approve_videos(self, request, queryset):
        queryset.update(active=True)

    def block_videos(self, request, queryset):
        queryset.update(active=False) 

class VideoReportAdmin(admin.ModelAdmin):
    list_display = ['reported_profile', 'reporting_profile', 'created_on', 'choice_reason', 'video_id']
    list_filter = ['created_on']
    search_fields = ['video__title', 'written_reason', 'choice_reason']

    def reported_profile(self, obj):
        return obj.video.profile
    reported_profile.short_description = 'Profile Reported'

    def reporting_profile(self, obj):
        return obj.profile
    reporting_profile.short_description = 'Profile Reporting'

admin.site.register(Video, VideoAdmin)
admin.site.register(VideoReport, VideoReportAdmin)