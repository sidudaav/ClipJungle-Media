from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ['profile', 'id', 'title', 'slug', 'count_categories', 'hot_score', 'created_on', 'active']
    list_filter = ['created_on']
    search_fields = ['user__username', 'title', 'categories__title']
    actions = ['approve_videos', 'block_videos']

    def count_categories(self, obj):
        return obj.categories.count()
    count_categories.short_description = 'Categories'

    def approve_videos(self, request, queryset):
        queryset.update(active=True)

    def block_videos(self, request, queryset):
        queryset.update(active=False) 

admin.site.register(Video, VideoAdmin)