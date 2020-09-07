from django.db import models
from profiles.models import Profile
from categories.models import Category
from taggit.managers import TaggableManager
from django.utils.text import slugify

class Video(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="videos_posted")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)

    slug = models.SlugField(unique=True, blank=True, max_length=100)
    tags = TaggableManager()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos")

    video_file = models.FileField(upload_to='video_files')
    created_on = models.DateTimeField(auto_now_add=True)

    hot_score = models.FloatField(null=True, blank=True)
    likes = models.ManyToManyField(Profile,
        related_name='videos_liked', blank=True)

    allow_comments = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
    
    def disable_comments(self):
        self.allow_comments = False

    class Meta:
        ordering = ('-created_on',)

class VideoReport(models.Model):
    SPAM = 1
    INAPPROPRIATE = 2
    OTHER = 3
    CHOICES = (
        (SPAM, 'Spam'),
        (INAPPROPRIATE, 'Inappropriate'),
        (OTHER, 'Other'),
    )

    profile = models.ForeignKey(Profile, related_name='videos_reported', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reports')
    choice_reason = models.SmallIntegerField(choices=CHOICES)
    written_reason = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} Reported {}'.format(self.user, self.video.user)