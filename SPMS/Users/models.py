from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersProfile(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_date_of_birth = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    user_sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    user_contact_number = models.CharField(max_length=15, null=True, blank=True)
    user_profile_picture = models.ImageField(upload_to="profile_pics", default="profile_pics/profile.jpg")

    def __str__(self):
        return f"{self.user.username} Profile"

