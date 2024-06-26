# Generated by Django 5.0.4 on 2024-04-18 05:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UsersProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_date_of_birth", models.DateField(verbose_name="Date of Birth")),
                (
                    "user_sex",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                (
                    "user_contact_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "user_profile_picture",
                    models.ImageField(
                        default="profile_pics/profile.jpg", upload_to="profile_pics"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
