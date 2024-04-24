from django.contrib import admin

from .models import StudentProfile, StudentFamilyRecords, StudentEducationalBackground, DocumentTypes, StudentDocuments

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(StudentFamilyRecords)
admin.site.register(StudentEducationalBackground)
admin.site.register(DocumentTypes)
admin.site.register(StudentDocuments)