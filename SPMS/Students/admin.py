from django.contrib import admin

from .models import StudentProfile, StudentFamilyRecords, StudentEducationalBackground

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(StudentFamilyRecords)
admin.site.register(StudentEducationalBackground)