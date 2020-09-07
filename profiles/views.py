from django.shortcuts import render, redirect, get_object_or_404

def register(request):
    return render(request, 'profiles/register.html')