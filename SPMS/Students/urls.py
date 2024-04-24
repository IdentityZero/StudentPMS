from django.urls import path

from .views import home, ProfileView, DocumentsView

urlpatterns = [
    path("", home, name='student-home'),
    path("profile", ProfileView.as_view(), name='student-profile'),
    path("documents", DocumentsView.as_view(), name='student-documents'),
]