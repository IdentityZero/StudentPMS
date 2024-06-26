# Generated by Django 5.0.4 on 2024-04-25 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Students", "0006_alter_studentdocuments_sd_date_uploaded"),
        ("University", "0003_rename_cirruculum_admissions_curriculum"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admissions",
            name="curriculum",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="University.curriculums"
            ),
        ),
        migrations.AlterField(
            model_name="courseprerequisite",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_toEnroll",
                to="University.courses",
            ),
        ),
        migrations.AlterField(
            model_name="courseprerequisite",
            name="prereq_course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="University.courses"
            ),
        ),
        migrations.AlterField(
            model_name="curriculumcourses",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="University.courses"
            ),
        ),
        migrations.AlterField(
            model_name="curriculumcourses",
            name="curriculum",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="University.curriculums"
            ),
        ),
        migrations.CreateModel(
            name="StudentGrades",
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
                    "grade",
                    models.CharField(
                        choices=[
                            ("1.00", "1.00"),
                            ("1.25", "1.25"),
                            ("1.50", "1.50"),
                            ("1.75", "1.75"),
                            ("2.00", "2.00"),
                            ("2.25", "2.25"),
                            ("2.50", "2.50"),
                            ("2.75", "2.75"),
                            ("3.00", "3.00"),
                            ("4.00", "4.00"),
                            ("5.00", "5.00"),
                            ("INC/5.00", "INC/5.00"),
                        ],
                        default="1.00",
                        max_length=16,
                    ),
                ),
                (
                    "SP",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Students.studentprofile",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="University.courses",
                    ),
                ),
            ],
        ),
    ]
