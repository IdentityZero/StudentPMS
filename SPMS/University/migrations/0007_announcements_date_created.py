# Generated by Django 5.0.4 on 2024-06-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("University", "0006_announcements_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="announcements",
            name="date_created",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
