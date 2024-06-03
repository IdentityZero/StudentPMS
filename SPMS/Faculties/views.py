from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from datetime import date
import json

from .models import FacultyProfile

from Users.models import UsersProfile
from Students.models import StudentProfile,StudentDocuments
from University.models import Admissions,CurriculumCourses, StudentGrades,Courses

# Create your views here.
@login_required
def home(request):
    user = request.user
    profile = UsersProfile.objects.get(user=user)
    try:
        faculty_profile = FacultyProfile.objects.get(profile=profile)
    except FacultyProfile.DoesNotExist:
        messages.info(request, 'Cannot access this platform.')
        logout(request)
        return redirect('login')
    return render(request, 'Faculties/home.html')


@login_required
def student_profiles(request):
    context = {}

    students = StudentProfile.objects.all()

    for student in students:
        student.admission = Admissions.objects.filter(SP=student).last()


    context['students'] = students

    return render(request, 'Faculties/student-profiles.html', context)


@login_required
def student_documents(request):
    context = {}

    documents = StudentDocuments.objects.all()
    print(documents.first().SP)

    context['documents'] = documents

    return render(request, 'Faculties/student-documents.html', context)


def retrieveStudentProfile(request):
    id = int(request.GET['id'])

    student_profile = StudentProfile.objects.get(id=id)

    data ={
        "id": id,
        "profile": {
            "university_email": student_profile.SP_univ_email,
            # "DOB": student_profile.profile.user_date_of_birth.strftime('%B %d, %Y'),
            "DOB": student_profile.profile.user_date_of_birth,
            "sex": student_profile.profile.user_sex,
            "contact": student_profile.profile.user_contact_number,
            "image": student_profile.profile.user_profile_picture.url,
            "first_name": student_profile.profile.user.first_name,
            "last_name": student_profile.profile.user.last_name,
            "full_name": student_profile.profile.user.get_full_name(),
            "username": student_profile.profile.user.username,
            "email": student_profile.profile.user.email
        }
    }

    return JsonResponse(data, status=200)


@csrf_exempt
def updateStudentPersonalInformation(request):
    if request.method == "GET":
        return JsonResponse({"error": "Invalid method"}, status=403)
    

    res = {}

    data = request.body
    data = json.loads(data)
    # unpack data
    id = int(data['id'])
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    univ_email = data['univ_email']
    dob = data['dob'].split("-")
    contact = data['contact']
    sex = data['sex']

    student_profile = StudentProfile.objects.get(id=id)
    user_profile = UsersProfile.objects.get(id=student_profile.profile.id)
    user = User.objects.get(id=student_profile.profile.user.id)
    
    try:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        student_profile.SP_univ_email = univ_email
        user_profile.user_date_of_birth = date(int(dob[0]),int(dob[1]), int(dob[2]))
        user_profile.user_contact_number = contact
        user_profile.user_sex = sex
        user_profile.save()
        user.save()
        student_profile.save()
    except IntegrityError:
        res['error'] = "Username already exists"
        return JsonResponse(res, status=200)
        
    res = {
        "id": id,
        "profile": {
            "university_email": univ_email,
            "DOB": dob,
            "sex": sex,
            "contact": contact,
            "image": user_profile.user_profile_picture.url,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": user.get_full_name(),
            "username": username,
            "email": email
        }
    }


    return JsonResponse(res, status=200)


def retrieveStudentGrades(request):
    id = int(request.GET['id'])

    student_profile = StudentProfile.objects.get(id=id)
    res = {}

    admission = Admissions.objects.filter(SP=student_profile).last()

    if not admission:
        return JsonResponse({"none": "No admission Records"}, status=200)

    grades = StudentGrades.objects.filter(SP=student_profile)
    curriculum = admission.curriculum
    curriculum_courses = CurriculumCourses.objects.filter(curriculum=curriculum)
    res = {}

    for course in curriculum_courses:
        # Get course prerequisite
        course.prereq = course.prerequisites()
        course.grade = grades.filter(course=course.course).last()

        year = course.year_level
        sem = course.semester

        if year not in res:
            res[year] = {}
           
        if sem not in res[year]:
            res[year][sem] = []
        
        prereq = []

        if course.prerequisites():
            for c in course.prerequisites():
                prereq.append(c.prereq_course.course_name)
        
        grade_id = None
        grade = None

        if grades.filter(course=course.course).last():
            grade_id = grades.filter(course=course.course).last().pk
            grade = str(grades.filter(course=course.course).last())
        
        res[year][sem].append({
            "name": course.course.course_name,
            "code": course.course.course_code,
            "prereq": prereq,
            "grade": {
                "id":grade_id,
                "value": grade
            },
            "id": course.course.id
        })

    return JsonResponse(res, status=200)


@csrf_exempt
def addEditStudentGrades(request):
    # this endpoit needs
    # Student profile id
    # course id
    # grades
    res = {
        "success" :"Added successfully!"
    }

    data = request.body
    data = json.loads(data)
    
    course_id = int(data['course_id'])
    student_id = int(data['student_id'])

    try:
        grade = float(data['grade'])
    except ValueError:
        grade = "INC/5.00"
    
    # Get course instance
    # Get student sintance
    course = Courses.objects.get(pk=course_id)
    student = StudentProfile.objects.get(pk=student_id)

    # Check if grades for this course already exist
    # If yes, edit
    # else, create

    grade_ins = StudentGrades.objects.filter(SP=student, course=course)

    if grade_ins:
        # update
        print("Update")
        grade_ins = grade_ins.first()
        print(grade_ins.course.course_name)
        grade_ins.grade = grade
        grade_ins.save()
    else:
        # Create
        print("Create")
        newGrade = StudentGrades.objects.create(SP=student,course=course,grade=grade)
        newGrade.save()

    res['grade'] = grade

    return JsonResponse(res,status=200)



