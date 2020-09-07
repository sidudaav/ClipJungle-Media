from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('success-page/', views.success_page, name='success-page')
]