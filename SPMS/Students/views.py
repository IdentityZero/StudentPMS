from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse


from itertools import groupby
from operator import itemgetter
import time
import json

from .forms import (UsersProfileEditForm, 
                    UserEditForm, 
                    StudentFamilyRecordsAddForm,
                    StudentFamilyRecordsEditForm,
                    EducationalBackgroundEditForm,
                    EducationalBackgroundAddForm, 
                    StudentDocumentEditForm,
                    StudentDocumentAddForm)

from .models import (StudentProfile, 
                    StudentFamilyRecords, 
                    StudentEducationalBackground,
                    StudentDocuments,
                    DocumentTypes)

from Users.models import UsersProfile
from University.models import Admissions,CurriculumCourses, StudentGrades, Announcements

# Create your views here.
@login_required
def home(request):

    announcements = Announcements.objects.filter(is_active=True).order_by('-date_created')

    context= {'announcements':announcements}
    user = request.user
    profile = UsersProfile.objects.get(user=user)
    try:
        student_profile = StudentProfile.objects.get(profile=profile)
    except StudentProfile.DoesNotExist:
        messages.info(request, 'Cannot access this platform')
        logout(request)
        return redirect('login')

    return render(request, 'Students/home.html',context)

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'Students/profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile_instance = UsersProfile.objects.get(user=user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)

        # User and User Profile Related
        context['baseProf_form'] = UsersProfileEditForm(instance=profile_instance)
        context['user_form'] = UserEditForm(instance=user)

        # Family Records Related
        # Get all data about student family
        family_records_QS = StudentFamilyRecords.objects.filter(SP=student_profile_instance)
        family_records_formset = modelformset_factory(StudentFamilyRecords, form=StudentFamilyRecordsEditForm, extra=0)
        # Set up forms
        context['family_records'] = family_records_QS
        context['editFamily_form'] = family_records_formset(queryset=family_records_QS)
        context['addFamily_form'] = StudentFamilyRecordsAddForm(instance=student_profile_instance)

        # Educational Background Related
        educ_bg_qs = StudentEducationalBackground.objects.filter(SP=student_profile_instance)
        educ_bg_formset = modelformset_factory(StudentEducationalBackground, form=EducationalBackgroundEditForm, extra=0)
        context['educBg_qs'] = educ_bg_qs
        context['editEducBg_fs'] = educ_bg_formset(queryset=educ_bg_qs)
        context['addEducBg_form'] = EducationalBackgroundAddForm(instance=student_profile_instance)
        

        return context

    def post(self,request,*args, **kwargs):
        user = self.request.user
        context = self.get_context_data(**kwargs)

        if 'email' in request.POST:
            # Returns the form if its invalid
            res = self.handleUserProfileEditForm(request)
        elif 'addFamilyRecordForm' in request.POST:
            res = self.handleAddFamilyMembersForm(request)
        elif 'editFamilyRecordForm' in request.POST:
            res = self.handleEditFamilyMembersForm(request)
        elif 'editEducationBackgroundForm' in request.POST:
            res = self.handleEditEducBgForm(request)
        elif 'addEducationalBackgroundForm' in request.POST:
            res = self.handleAddEducBgForm(request)
        
        if res == 0:
            return HttpResponseRedirect(reverse('student-profile'))
        else:
            context.update(res)

        return render(request, self.template_name, context)

    def handleUserProfileEditForm(self,request):
        user = request.user
        profile_instance = UsersProfile.objects.get(user=user)
        baseProf_form = UsersProfileEditForm(request.POST, request.FILES,instance=profile_instance)
        user_form = UserEditForm(request.POST, instance=user)
        if baseProf_form.is_valid() and user_form.is_valid():
            baseProf_form.save()
            user_form.save()
            return 0

        return {
            'baseProf_form': baseProf_form,
            'user_form': user_form,
        }

    def handleAddFamilyMembersForm(self,request):
        user = request.user
        profile_instance = UsersProfile.objects.get(user=user)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)
        addFamily_form = StudentFamilyRecordsAddForm(request.POST,instance=student_profile_instance)
        if addFamily_form.is_valid():
            # Unpack the forms
            sp_relationship = addFamily_form.cleaned_data['SP_relationship']
            sp_fam_first_name = addFamily_form.cleaned_data['SP_fam_first_name']
            sp_fam_last_name = addFamily_form.cleaned_data['SP_fam_last_name']
            sp_fam_contact_number = addFamily_form.cleaned_data['SP_fam_contact_number']
            sp_fam_emergency_contact = addFamily_form.cleaned_data['SP_fam_emergency_contact']

            new_fam = StudentFamilyRecords.objects.create(
                SP = student_profile_instance,
                SP_relationship = sp_relationship,
                SP_fam_first_name = sp_fam_first_name,
                SP_fam_last_name = sp_fam_last_name,
                SP_fam_contact_number = sp_fam_contact_number,
                SP_fam_emergency_contact = sp_fam_emergency_contact
            )

            new_fam.save()
            
            return 0
        
        return {
            'addFamily_form': addFamily_form
        }
    
    def handleEditFamilyMembersForm(self, request):
        # !TODO
        # JS WILL HANDLE THE ERRORS FOR THIS FORM
        id = request.POST.get('id')
        fam_inst = StudentFamilyRecords.objects.get(id=id)
        editFamily_form = StudentFamilyRecordsEditForm(request.POST, instance=fam_inst)

        if editFamily_form.is_valid():
            editFamily_form.save()
            return 0

        profile_instance = UsersProfile.objects.get(user=request.user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)
        # Get all data about student family
        family_records_QS = StudentFamilyRecords.objects.filter(SP=student_profile_instance)
        family_records_formset = modelformset_factory(StudentFamilyRecords, form=StudentFamilyRecordsEditForm, extra=0)
        
        return {
            'editFamily_form':family_records_formset(queryset=family_records_QS)
        }

    def handleEditEducBgForm(self,request):
        id = request.POST.get('id')
        educBg_ins = StudentEducationalBackground.objects.get(id=id)
        educBg_form = EducationalBackgroundEditForm(request.POST, instance=educBg_ins)

        if educBg_form.is_valid():
            educBg_form.save()
            return 0

        profile_instance = UsersProfile.objects.get(user=request.user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)
        educ_bg_qs = StudentEducationalBackground.objects.filter(SP=student_profile_instance)
        educ_bg_formset = modelformset_factory(StudentEducationalBackground, form=EducationalBackgroundEditForm, extra=0)

        return {
            'editEducBg_fs': educ_bg_formset(queryset=educ_bg_qs)
        }

    def handleAddEducBgForm(self,request):
        user = request.user
        profile_instance = UsersProfile.objects.get(user=user)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)
        addEducBg_form = EducationalBackgroundAddForm(request.POST, instance=student_profile_instance)

        if addEducBg_form.is_valid():
            # Unpack the forms
            sp_education_level = addEducBg_form.cleaned_data['SP_education_level']
            sp_institution = addEducBg_form.cleaned_data['SP_institution']
            sp_address = addEducBg_form.cleaned_data['SP_address']
            sp_description = addEducBg_form.cleaned_data['SP_description']
            sp_last_year_attended = addEducBg_form.cleaned_data['SP_last_year_attended']

            new_educBg = StudentEducationalBackground.objects.create(
                SP=student_profile_instance,
                SP_education_level=sp_education_level,
                SP_institution=sp_institution,
                SP_address=sp_address,
                SP_description=sp_description,
                SP_last_year_attended=sp_last_year_attended,
            )

            new_educBg.save()
            return 0

        return {
            'addEducBg_form': addEducBg_form
        }


class DocumentsView(LoginRequiredMixin, TemplateView):
    template_name = 'Students/documents.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_instance = UsersProfile.objects.get(user=user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)

        # Get all documents
        all_docs = StudentDocuments.objects.filter(SP=student_profile_instance)
        context['all_docs_qs'] = all_docs

        # Edit Documents
        editDocs_formset = modelformset_factory(StudentDocuments,form=StudentDocumentEditForm, extra=0)
        context['editDocs_fs'] = editDocs_formset(queryset=all_docs)

        # Add Documents
        context['addDocs_form'] = StudentDocumentAddForm(instance=student_profile_instance)

        return context
    
    def post(self,request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user

        form_label = request.POST.get('formLabel')

        if form_label == "StudentDocumentEditForm":
            res = self.handleEditStudentDocuments(request)
        elif form_label == "StudentDocumentAddForm":
            res = self.handleAddStudentDocuments(request)
        

        if res == 0:
            return HttpResponseRedirect(reverse('student-documents'))
        else:
            context.update(res)

        return render(request, self.template_name, context)

    def handleEditStudentDocuments(self,request):
        id = request.POST.get('id')
        instance = StudentDocuments.objects.get(id=id)
        
        form = StudentDocumentEditForm(request.POST,request.FILES,instance=instance)

        if form.is_valid:
            form.save()
            return 0
        
        user = self.request.user
        profile_instance = UsersProfile.objects.get(user=user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)

        # Get all documents
        all_docs = StudentDocuments.objects.filter(SP=student_profile_instance)
        
        editDocs_formset = modelformset_factory(StudentDocuments,form=StudentDocumentEditForm, extra=0)

        return {
            'editDocs_fs': editDocs_formset(queryset=all_docs)
        }

    def handleAddStudentDocuments(self,request):
        user = request.user
        profile_instance = UsersProfile.objects.get(user=user)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)

        form = StudentDocumentAddForm(request.POST, request.FILES, instance=student_profile_instance)

        if form.is_valid():
            # Unpack
            document_type = DocumentTypes.objects.get(document_type=form.cleaned_data['SD_doc_type'])
            document = request.FILES['SD_document']

            new_doc = StudentDocuments.objects.create(
                SP=student_profile_instance,
                SD_doc_type=document_type,
                SD_document=document
            )
            new_doc.save()

            return 0
        
        return {
            'addDocs_form': form
        }


class GradesView(LoginRequiredMixin, TemplateView):
    template_name = 'Students/grades.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_instance = UsersProfile.objects.get(user=user.id)
        student_profile_instance = StudentProfile.objects.get(profile=profile_instance)

        # Get admissions
        admission = Admissions.objects.filter(SP=student_profile_instance).last()
        context['admission'] = admission

        if not admission:
            # Not enrolled
            return context
        
        # Get student grades
        grades = StudentGrades.objects.filter(SP=student_profile_instance)

        # Get curriculum courses
        curriculum = admission.curriculum # Get curriculum
        curriculum_courses = CurriculumCourses.objects.filter(curriculum=curriculum)   # Get curriculum courses

        grouped_courses = {}

        for course in curriculum_courses:
            # Get course prerequisite
            course.prereq = course.prerequisites()
            course.grade = grades.filter(course=course.course).last()

            key = (course.year_level, course.semester)
            
            if key not in grouped_courses:
                grouped_courses[key] = []
            grouped_courses[key].append(course)
        
        context['curriculum_courses'] = grouped_courses

        return context

@csrf_exempt
def deleteDocuments(request):

    data = json.loads(request.body)
    doc_id = int(data['doc'])

    doc_ins = StudentDocuments.objects.get(id=doc_id)
    doc_ins.delete()

    res = {
        "message": "Document Deleted"
    }
    return JsonResponse(res, status=200)






