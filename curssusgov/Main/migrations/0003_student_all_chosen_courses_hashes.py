# Generated by Django 4.2.5 on 2023-09-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_alter_university_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='all_chosen_courses_hashes',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
