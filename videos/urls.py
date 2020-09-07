from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('home/', views.home, name='home')
]