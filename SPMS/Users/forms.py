from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UsersProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name' ,'last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UsersProfile
        fields = ['user_date_of_birth', 'user_sex', 'user_contact_number', 'user_profile_picture']