from django.db import models

from Students.models import StudentProfile

# Create your models here.
class Courses(models.Model):
    course_code = models.CharField(unique=True, max_length=32)
    course_name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Courses, models.CASCADE, related_name="course_toEnroll")
    prereq_course = models.ForeignKey(Courses, models.CASCADE)

    def __str__(self):
        return f"Course: {self.course} | Prerequisite: {self.prereq_course}"


class Departments(models.Model):
    department_name = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return self.department_name


class Degrees(models.Model):
    department = models.ForeignKey(Departments, models.DO_NOTHING)
    degree_name = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return self.degree_name


class Curriculums(models.Model):
    degree = models.ForeignKey(Degrees, models.DO_NOTHING)
    curriculum_name = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return self.curriculum_name


class CurriculumCourses(models.Model):
    SEMESTER_CHOICES = [
        ("First", "First Semester"),
        ("Second", "Second Semester"),
        ("Mid Year", "Mid Year"),
    ]

    curriculum = models.ForeignKey(Curriculums, models.CASCADE)
    course = models.ForeignKey(Courses, models.CASCADE)
    year_level = models.IntegerField()
    semester = models.CharField(max_length=16, choices=SEMESTER_CHOICES, default='First')

    def prerequisites(self):
        return CoursePrerequisite.objects.filter(course=self.course)


class Admissions(models.Model):
    SP = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculums, on_delete=models.CASCADE)


class Enrollments(models.Model):
    SEMESTER_CHOICES = [
        ("First", "First Semester"),
        ("Second", "Second Semester"),
        ("Mid Year", "Mid Year"),
    ]
    admission = models.ForeignKey(Admissions, on_delete=models.CASCADE)
    year_level = models.IntegerField()
    semester = models.CharField(max_length=16, choices=SEMESTER_CHOICES, default='First')


class CoursesEnrolled(models.Model):
    enrollment = models.ForeignKey(Enrollments, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


class StudentGrades(models.Model):
    GRADE_CHOICES = [
        ("1.00", "1.00"),
        ("1.25", "1.25"),
        ("1.50", "1.50"),
        ("1.75", "1.75"),
        ("2.00", "2.00"),
        ("2.25", "2.25"),
        ("2.50", "2.50"),
        ("2.75", "2.75"),
        ("3.00", "3.00"),
        ("4.00", "4.00"),
        ("5.00", "5.00"),
        ("INC/5.00", "INC/5.00"),
    ]
    SP = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    grade = models.CharField(max_length=16,choices=GRADE_CHOICES, default="1.00")

