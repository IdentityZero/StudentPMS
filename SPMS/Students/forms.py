from django import forms
from django.contrib.auth.models import User


from .models import StudentProfile, StudentFamilyRecords, StudentEducationalBackground, StudentDocuments
from Users.models import UsersProfile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UsersProfileEditForm(forms.ModelForm):
    class Meta:
        model = UsersProfile
        fields = ['user_date_of_birth', 'user_sex', 'user_contact_number', 'user_profile_picture']
        labels = {
            'user_date_of_birth': 'Date of Birth',
            'user_sex': 'Sex',
            'user_contact_number': 'Contact Number',
            'user_profile_picture': 'Profile Picture',
        }


class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['SP_univ_email']


class StudentFamilyRecordsAddForm(forms.ModelForm):
    addFamilyRecordForm = forms.CharField(widget=forms.HiddenInput(), initial='addFamilyRecordForm')
    class Meta:
        model = StudentFamilyRecords
        fields = ['SP_relationship','SP_fam_first_name', 'SP_fam_last_name', 'SP_fam_contact_number', 'SP_fam_emergency_contact']
        labels = {
            'SP_relationship': 'Relationship',
            'SP_fam_first_name': 'First Name',
            'SP_fam_last_name': 'Last Name',
            'SP_fam_contact_number': 'Contact Number',
            'SP_fam_emergency_contact': 'Set as Emergency Contact',
        }


class StudentFamilyRecordsEditForm(forms.ModelForm):
    editFamilyRecordForm = forms.CharField(widget=forms.HiddenInput(), initial='editFamilyRecordForm')
    class Meta:
        model = StudentFamilyRecords
        fields = ['SP_relationship','SP_fam_first_name', 'SP_fam_last_name', 'SP_fam_contact_number', 'SP_fam_emergency_contact']
        labels = {
            'SP_relationship': 'Relationship',
            'SP_fam_first_name': 'First Name',
            'SP_fam_last_name': 'Last Name',
            'SP_fam_contact_number': 'Contact Number',
            'SP_fam_emergency_contact': 'Set as Emergency Contact',
        }

    def add_prefix(self, field_name):
        return field_name  # Override add_prefix to return the field name as is during formsets


class EducationalBackgroundEditForm(forms.ModelForm):
    editEducationBackgroundForm = forms.CharField(widget=forms.HiddenInput(), initial='editEducationBackgroundForm')
    class Meta:
        model = StudentEducationalBackground
        fields = ['SP_education_level', 'SP_institution', 'SP_address', 'SP_description', 'SP_last_year_attended']
        labels = {
            'SP_education_level': 'Level',
            'SP_institution': 'Institution',
            'SP_address': 'Address',
            'SP_description': 'Description',
            'SP_last_year_attended': 'Graduated/Last Year Attended'
        }
    
    def __init__(self, *args, **kwargs):
        super(EducationalBackgroundEditForm, self).__init__(*args, **kwargs)
        self.fields['SP_last_year_attended'].help_text = ''
    
    def add_prefix(self, field_name):
        return field_name  # Override add_prefix to return the field name as is during formsets


class EducationalBackgroundAddForm(forms.ModelForm):
    addEducationalBackgroundForm = forms.CharField(widget=forms.HiddenInput(), initial='addEducationalBackgroundForm')
    class Meta:
        model = StudentEducationalBackground
        fields = ['SP_education_level', 'SP_institution', 'SP_address', 'SP_description', 'SP_last_year_attended']
        labels = {
            'SP_education_level': 'Level',
            'SP_institution': 'Institution',
            'SP_address': 'Address',
            'SP_description': 'Description',
            'SP_last_year_attended': 'Graduated/Last Year Attended'
        }

    def __init__(self, *args, **kwargs):
        super(EducationalBackgroundAddForm, self).__init__(*args, **kwargs)
        self.fields['SP_last_year_attended'].help_text = ''


class StudentDocumentEditForm(forms.ModelForm):
    formLabel = forms.CharField(widget=forms.HiddenInput(), initial='StudentDocumentEditForm')
    class Meta:
        model = StudentDocuments
        fields = ['SD_doc_type', 'SD_document']
        labels = {
            'SD_doc_type': "Document Type",
            'SD_document': "File",
        }

        widgets = {
            'SD_doc_type': forms.Select(attrs={'required': 'required'})
        }

    def add_prefix(self, field_name):
        return field_name  # Override add_prefix to return the field name as is during formsets


class StudentDocumentAddForm(forms.ModelForm):
    formLabel = forms.CharField(widget=forms.HiddenInput(), initial='StudentDocumentAddForm')
    class Meta:
        model = StudentDocuments
        fields = ['SD_doc_type', 'SD_document']
        labels = {
            'SD_doc_type': "Document Type",
            'SD_document': "File",
        }

        widgets = {
            'SD_doc_type': forms.Select(attrs={'required': 'required'})
        }



