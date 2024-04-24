from django.db import models

from Users.models import UsersProfile

# Create your models here.
# SP = StudentProfile
class StudentProfile(models.Model):
    profile = models.OneToOneField(UsersProfile, on_delete=models.CASCADE)
    SP_univ_email = models.EmailField(unique=True,null=True, blank=True)


class StudentFamilyRecords(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Guardian','Guardian'),
        ('Father','Father'),
        ('Mother','Mother'),
        ('Sibling','Sibling'),
        ('Spouse','Spouse'),
    ]
    SP = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    SP_relationship = models.CharField(max_length=16, choices=RELATIONSHIP_CHOICES, default='Guardian')
    SP_fam_first_name = models.CharField(max_length=64)
    SP_fam_last_name = models.CharField(max_length=64)
    SP_fam_contact_number = models.CharField(max_length=15)
    SP_fam_emergency_contact = models.BooleanField(default=False)


class StudentEducationalBackground(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('Primary', 'Primary Level'),
        ('Secondary', 'Secondary Level'),
        ('Tertiary', 'Tertiary Level'),
        ('Vocational', 'Vocational'),
        ('Post-Graduate', 'Post-Graduate'),
    ]

    SP = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    SP_education_level = models.CharField(max_length=32, choices=EDUCATION_LEVEL_CHOICES, default='Primary')
    SP_institution = models.CharField(max_length=256)
    SP_address = models.CharField(max_length=256)
    SP_description = models.TextField(blank=True, null=True)
    SP_last_year_attended = models.IntegerField('Year', help_text="Year graduated or last year attended")


class DocumentTypes(models.Model):
    document_type = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.document_type


class StudentDocuments(models.Model):
    SP = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    SD_doc_type = models.ForeignKey(DocumentTypes, models.DO_NOTHING)
    SD_document = models.FileField(upload_to="documents", blank=True, null=True)
    SD_date_uploaded = models.DateTimeField(auto_now=True)


