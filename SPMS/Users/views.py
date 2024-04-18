from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import UserRegistrationForm

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
            form.save()
            return redirect('login')
        else:
            messages
    else:
        form = UserRegistrationForm()
    context['form'] = form

    return render(request, 'Users/register.html', context)

