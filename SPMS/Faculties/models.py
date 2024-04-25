from django.db import models

from Users.models import UsersProfile

# Create your models here.
class FacultyProfile(models.Model):
    profile = models.OneToOneField(UsersProfile, on_delete=models.CASCADE)
    FP_univ_email = models.EmailField(unique=True,null=True, blank=True)

    def __str__(self):
        return self.profile.user.username