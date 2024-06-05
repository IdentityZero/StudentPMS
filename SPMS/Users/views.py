from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.http import HttpResponse


from Students.models import StudentProfile
from Faculties.models import FacultyProfile

from University.models import Admissions, Curriculums

from .forms import UserRegistrationForm
from .models import UsersProfile


# Create your views here.
def home_redirect(request):
    """
    This view will check if the client is a student or a faculty.
    If it does not have a profile, put back to login to contact admin.
    """

    return redirect('student-home')


def register(request):
    context = {}

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Valid")
            form.save()

            # Get user instance
            user_name = request.POST.get('username') 
            user = User.objects.get(username=user_name)

            # Create a profile for the user
            profile = UsersProfile.objects.create(user=user)
            profile.save()

            # Create Student profile or Faculty Profile
            role = request.POST.get('roles')
            if role == "Faculty":
                # Create Faculty Profile
                faculty_profile = FacultyProfile.objects.create(profile=profile)
                faculty_profile.save()
            else:
                # Create Student Profile
                student_profile = StudentProfile.objects.create(profile=profile)
                student_profile.save()

                # Save admission
                curriculum = Curriculums.objects.first()
                Admissions.objects.create(SP=student_profile, curriculum=curriculum)

        else:
            print(form.errors)

    else:
        form = UserRegistrationForm()
    context['form'] = form

    return render(request, 'Users/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            if role == "Student":
                return redirect("student-home")
            else:
                return redirect("faculty-home")
            return redirect('home-redirect')
        else:
            messages.success(request, "Incorrect Username or Password")
            return redirect('login')
        
    
    return render(request, "Users/login.html")


