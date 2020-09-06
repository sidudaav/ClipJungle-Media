from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='category_pics')

    total_videos = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)


    class Meta:
            ordering = ('-total_views',)
            verbose_name_plural = 'Categories'
    
    def __str__(self):
            return f'{self.title}'