# Generated by Django 5.0.4 on 2024-04-18 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Users", "0003_alter_usersprofile_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentProfile",
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
                (
                    "SP_univ_email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.usersprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentFamilyRecords",
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
                ("SP_fam_first_name", models.CharField(max_length=64)),
                ("SP_fam_last_name", models.CharField(max_length=64)),
                ("SP_fam_contact_number", models.CharField(max_length=15)),
                ("SP_fam_emergency_contact", models.BooleanField(default=False)),
                (
                    "SP",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Students.studentprofile",
                    ),
                ),
            ],
        ),
    ]
