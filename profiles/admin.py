from django.contrib import admin
from .models import Profile, ProfileFollowRequest, ProfileFollowing, IssueReport, ProfileBlock

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileFollowing)
admin.site.register(ProfileFollowRequest)
admin.site.register(ProfileBlock)
admin.site.register(IssueReport)