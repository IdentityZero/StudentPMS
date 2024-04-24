from django.urls import path

from .views import home, ProfileView

urlpatterns = [
    path("", home, name='student-home'),
    path("profile", ProfileView.as_view(), name='student-profile'),
]