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