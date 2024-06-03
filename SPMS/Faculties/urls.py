from django.urls import path

from .views import home, student_profiles,retrieveStudentProfile,updateStudentPersonalInformation,retrieveStudentGrades,addEditStudentGrades,student_documents

urlpatterns = [
    path("", home, name='faculty-home'),
    path("student_profiles/", student_profiles, name='faculty-student-profiles'),
    path("student_documents/", student_documents, name='faculty-student-documents'),
    path("student_profiles/detail/", retrieveStudentProfile),
    path("student_profiles/update/", updateStudentPersonalInformation),
    path("student_profiles/grades/", retrieveStudentGrades),
    path("student_profiles/grades/update/", addEditStudentGrades),
]