# Generated by Django 5.0.4 on 2024-04-24 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Students", "0003_studenteducationalbackground"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentTypes",
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
                ("document_type", models.CharField(max_length=256, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
    ]