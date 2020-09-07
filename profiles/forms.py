from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, IssueReport

YEARS= [x for x in range(1940,2021)]

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        required=True,
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        required=True,
    )

    username = forms.CharField(
        label='Username',
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        label='Email',
        max_length=150,
        required=True,
    )

    password1 = forms.CharField(
        label='Password',
        max_length=100,
        required=True
    )

    password2 = forms.CharField(
        label='Confirm Password',
        max_length=100,
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        required=True,
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        required=True,
    )

    username = forms.CharField(
        label='Username',
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        label='Email',
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'public', 'image']

class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['body']