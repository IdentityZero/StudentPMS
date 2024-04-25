from django.contrib import admin

from .models import (Courses,
                     CoursePrerequisite,
                     Departments,
                     Degrees,
                     Curriculums,
                     CurriculumCourses,
                     Admissions,
                     Enrollments,
                     CoursesEnrolled,
                     StudentGrades)

# Register your models here.

class CurriculumColumn(admin.ModelAdmin):
    list_display = ['degree','curriculum_name']


class CoursesColumn(admin.ModelAdmin):
    list_display = ['course_code','course_name']


class CurriculumCoursesColumn(admin.ModelAdmin):
    list_display = ['curriculum','course', 'year_level', 'semester']


class AdmissionsColumn(admin.ModelAdmin):
    list_display = ['SP','curriculum']


class StudentGradesColumn(admin.ModelAdmin):
    list_display = ['SP','course']


admin.site.register(Courses, CoursesColumn)
admin.site.register(CoursePrerequisite)
admin.site.register(Departments)
admin.site.register(Degrees)
admin.site.register(Curriculums, CurriculumColumn)
admin.site.register(CurriculumCourses,CurriculumCoursesColumn)
admin.site.register(Admissions, AdmissionsColumn)
admin.site.register(Enrollments)
admin.site.register(CoursesEnrolled)
admin.site.register(StudentGrades, StudentGradesColumn)


