# Generated by Django 4.0.4 on 2022-08-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLearnApp', '0008_remove_student_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=None),
        ),
    ]