# Generated by Django 4.0.4 on 2022-07-03 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLearnApp', '0003_course_interested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='interested',
        ),
    ]
