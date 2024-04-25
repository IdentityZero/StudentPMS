from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import FacultyProfile
from Users.models import UsersProfile

# Create your views here.
@login_required
def home(request):
    user = request.user
    profile = UsersProfile.objects.get(user=user)
    try:
        faculty_profile = FacultyProfile.objects.get(profile=profile)
    except FacultyProfile.DoesNotExist:
        messages.info(request, 'Not a Faculty! Cannot access this platform.')
        logout(request)
        return redirect('login')
    return render(request, 'Faculties/home.html')

