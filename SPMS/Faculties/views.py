from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from datetime import date, timedelta
import json

from .models import FacultyProfile

from Users.models import UsersProfile
from Students.models import StudentProfile,StudentDocuments,StudentFamilyRecords,StudentEducationalBackground,DocumentTypes
from Students.serializers import StudentDocumentsSerializer,DocumentTypesSerializer
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
    document_types = DocumentTypes.objects.all()

    context['documents'] = documents
    context['document_types'] = document_types

    return render(request, 'Faculties/student-documents.html', context)


def retrieveStudentDocuments(request):
    res = {}

    documents = StudentDocuments.objects.all()

    if 'username' in request.GET:
        username = request.GET['username']
        students = StudentProfile.objects.filter(profile__user__username__icontains=username)
        documents = documents.filter(SP__in=students)
        
    if 'type' in request.GET:
        type = request.GET['type']
        doc_type = DocumentTypes.objects.get(pk=type)
        documents = documents.filter(SD_doc_type=doc_type)
    
    if 'ext' in request.GET:
        ext = f".{request.GET['ext']}"
        documents = documents.filter(SD_document__endswith=ext)

    if 'date' in request.GET:
        date = int(request.GET['date'])
        date_filter = (timezone.now() - timedelta(days=date)).date()
        documents = documents.filter(SD_date_uploaded__date=date_filter)


    serializer = StudentDocumentsSerializer(documents, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def updateDocument(request):
    res = {}

    data = request.POST
    file = request.FILES

    id = int(data['id'])
    type = int(data['type'])
    comment = data['comment']
    clear = data['clear']

    # Get Document instance
    document = StudentDocuments.objects.get(pk=id)
    document_type = DocumentTypes.objects.get(pk=type)

    document.SD_doc_type = document_type
    document.SD_comment = comment

    if clear == "true":
        document.SD_document.delete()
        document.SD_document = None
    
    if file:
        document.SD_document = file['file']

    document.save()
    serializer = StudentDocumentsSerializer(document)

    res['message'] = "OK"
    res['updated'] = serializer.data
    return JsonResponse(res, status=200)
    







@csrf_exempt
def addNewDocumentType(request):
    res = {}

    data = request.body
    data = json.loads(data)

    # unpack data
    type = data['type']
    description = data['description']

    try:
        DocumentTypes.objects.create(document_type=type, description=description)
        res['success'] = ["OK"]
    except IntegrityError:

        res['error'] = "Document Type Already exists!"
    
    type= DocumentTypes.objects.all()

    serializer = DocumentTypesSerializer(type, many=True)
    res['updated'] = serializer.data 

    return JsonResponse(res, status=200)


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


def retrieveStudentFamilyRecords(request):
    res ={}

    # Get student profile
    id = int(request.GET['id'])
    student_profile = StudentProfile.objects.get(id=id)
    res['id'] = id

    fam_records = StudentFamilyRecords.objects.filter(SP=student_profile)
    fam_records_arr = []

    for record in fam_records:
        fam_record_dict = {
            "id": record.id,
            "relationship": record.SP_relationship,
            "first_name": record.SP_fam_first_name,
            "last_name": record.SP_fam_last_name,
            "contact": record.SP_fam_contact_number,
            "emergency_contact": record.SP_fam_emergency_contact
        }
        fam_records_arr.append(fam_record_dict)
    
    res['results'] = fam_records_arr
    return JsonResponse(res, status=200)


@csrf_exempt
def addStudentFamilyRecords(request):
    res = {}

    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    relationship = data['relationship']
    contact = data['contact']
    first_name = data['first_name']
    last_name = data['last_name']
    emergency = data['emergency']
    if emergency == "true":
        emergency = True
    else:
        emergency = False
    
    student_profile_ins = StudentProfile.objects.get(pk=id)

    record =StudentFamilyRecords.objects.create(
        SP=student_profile_ins,
        SP_relationship=relationship,
        SP_fam_first_name=first_name,
        SP_fam_last_name=last_name,
        SP_fam_contact_number = contact,
        SP_fam_emergency_contact=emergency
    )

    record.save()
    res['success'] = "OK"
    return JsonResponse(res, status=200)

@csrf_exempt
def updateStudentFamilyRecords(request):
    # this end point will receive
    # relationship, first name, last name, contact number, and emergency
    res = {}

    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    relationship = data['relationship']
    contact = data['contact']
    first_name = data['first_name']
    last_name = data['last_name']
    emergency = data['emergency']
    if emergency == "true":
        emergency = True
    else:
        emergency = False

    record =StudentFamilyRecords.objects.get(pk=id)

    record.SP_relationship = relationship
    record.SP_fam_first_name = first_name
    record.SP_fam_last_name = last_name
    record.SP_fam_contact_number = contact
    record.SP_fam_emergency_contact = emergency
    record.save()

    res['success'] = "OK"
    return JsonResponse(res, status=200)


@csrf_exempt
def deleteStudentFamilyRecords(request):
    # This endpoint will receive an id of the family record
    res = {}
    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    record =StudentFamilyRecords.objects.get(pk=id)
    record.delete()

    res['success'] = "OK"
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

        grade_ins = grade_ins.first()
        grade_ins.grade = grade
        grade_ins.save()
    else:
        # Create
        newGrade = StudentGrades.objects.create(SP=student,course=course,grade=grade)
        newGrade.save()

    res['grade'] = grade

    return JsonResponse(res,status=200)


def retrieveStudentEducationBG(request):
    res = {}
    id = int(request.GET['id'])
    student_profile = StudentProfile.objects.get(id=id)
    res['id'] = id

    educ_records = StudentEducationalBackground.objects.filter(SP=student_profile)
    educ_records_arr = []

    for record in educ_records:
        educ_record_dict = {
            "id": record.id,
            "level": record.SP_education_level,
            "institution": record.SP_institution,
            "address": record.SP_address,
            "description" : record.SP_description,
            "year": record.SP_last_year_attended
        }
        educ_records_arr.append(educ_record_dict)
    
    res['results'] = educ_records_arr


    return JsonResponse(res, status=200)

@csrf_exempt
def addStudentEducationBG(request):
    res = {}

    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    level = data['level']
    institution = data['institution']
    address = data['address']
    description = data['description']
    year = int(data['year'])

    student_profile_ins = StudentProfile.objects.get(pk=id)

    record = StudentEducationalBackground.objects.create(
        SP=student_profile_ins,
        SP_education_level=level,
        SP_institution=institution,
        SP_address=address,
        SP_description=description,
        SP_last_year_attended=year,
    )

    record.save()

    res['success'] = "OK"
    return JsonResponse(res, status=200)

@csrf_exempt
def updateStudentEducationBG(request):
    # This endpoint will accept
    # level, institution, address, description, year
    res = {}

    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    level = data['level']
    institution = data['institution']
    address = data['address']
    description = data['description']
    year = int(data['year'])

    record =StudentEducationalBackground.objects.get(pk=id)

    record.SP_education_level = level
    record.SP_institution = institution
    record.SP_address = address
    record.SP_description = description
    record.SP_last_year_attended = year
    record.save()

    res['success'] = "OK"
    return JsonResponse(res, status=200)


@csrf_exempt
def deleteStudentEducationBG(request):
    res = {}
    data = request.body
    data = json.loads(data)

    # unpack data
    id = int(data['id'])
    record =StudentEducationalBackground.objects.get(pk=id)
    record.delete()

    res['success'] = "OK"
    return JsonResponse(res, status=200)

