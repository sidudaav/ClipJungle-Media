from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name="logout"),
    path('auth/activate/<uidb64>/<token>/', views.activate, name='activate')
]