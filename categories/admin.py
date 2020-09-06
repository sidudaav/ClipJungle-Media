from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'total_videos', 'total_views', 'total_likes']
    search_fields = ['title']

admin.site.register(Category, CategoryAdmin)