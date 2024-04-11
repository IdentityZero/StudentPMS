from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersProfile(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, models.DO_NOTHING)
    user_date_of_birth = models.DateField(verbose_name="Date of Birth", null=False, blank=False)
    user_sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    user_contact_number = models.CharField(max_length=15, null=True, blank=True)
    user_profile_picture = models.ImageField(upload_to="profile_pics", default="profile_pics/profile.jpg")