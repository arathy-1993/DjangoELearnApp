# Generated by Django 4.0.4 on 2022-07-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLearnApp', '0004_remove_course_interested'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
