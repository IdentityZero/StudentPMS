from django.urls import path

from .views import (home, 
                    student_profiles,
                    student_documents,

                    retrieveStudentProfile,
                    updateStudentPersonalInformation,

                    retrieveStudentGrades,
                    addEditStudentGrades,

                    retrieveStudentFamilyRecords,
                    addStudentFamilyRecords,
                    updateStudentFamilyRecords,
                    deleteStudentFamilyRecords,

                    retrieveStudentEducationBG,
                    addStudentEducationBG,
                    updateStudentEducationBG,
                    deleteStudentEducationBG,
                    
                    retrieveStudentDocuments,
                    addNewDocumentType,
                    updateDocument)

urlpatterns = [
    path("", home, name='faculty-home'),
    path("student_profiles/", student_profiles, name='faculty-student-profiles'),
    path("student_documents/", student_documents, name='faculty-student-documents'),
    path("student_documents/filter/", retrieveStudentDocuments),
    path("student_documents/type/add/", addNewDocumentType),
    path("student_documents/update/", updateDocument),
    path("student_profiles/detail/", retrieveStudentProfile),
    path("student_profiles/update/", updateStudentPersonalInformation),
    path("student_profiles/grades/", retrieveStudentGrades),
    path("student_profiles/grades/update/", addEditStudentGrades),
    path("student_profiles/family/", retrieveStudentFamilyRecords),
    path("student_profiles/family/add/", addStudentFamilyRecords),
    path("student_profiles/family/update/", updateStudentFamilyRecords),
    path("student_profiles/family/delete/", deleteStudentFamilyRecords),
    path("student_profiles/education/", retrieveStudentEducationBG),
    path("student_profiles/education/add/", addStudentEducationBG),
    path("student_profiles/education/update/", updateStudentEducationBG),
    path("student_profiles/education/delete/", deleteStudentEducationBG),
]