from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='', blank=True, max_length=500)

    public = models.BooleanField(default=True)

    total_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

class IssueReport(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="issues_reported")
    body = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

class ProfileFollowRequest(models.Model):
    profile_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follow_requests_sent')
    profile_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follot_requests_received')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

class ProfileFollowing(models.Model):
    profile_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    profile_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

class ProfileBlock(models.Model):
    profile_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocking')
    profile_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blockers')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)
