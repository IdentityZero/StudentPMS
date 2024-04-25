from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UsersProfile


class UserRegistrationForm(UserCreationForm):
    ROLES = (
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    )
    roles = forms.ChoiceField(choices=ROLES, widget=forms.Select)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name' ,'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Student ID'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UsersProfile
        fields = ['user_date_of_birth', 'user_sex', 'user_contact_number', 'user_profile_picture']