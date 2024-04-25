from django.urls import path

from .views import home, ProfileView, DocumentsView,GradesView

urlpatterns = [
    path("", home, name='student-home'),
    path("profile", ProfileView.as_view(), name='student-profile'),
    path("documents", DocumentsView.as_view(), name='student-documents'),
    path("grades", GradesView.as_view(), name='student-grades')
]