# Generated by Django 4.2.5 on 2023-09-15 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_student_all_chosen_courses_hashes'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='admission_processed',
            field=models.BooleanField(default=False),
        ),
    ]
