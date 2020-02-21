# Generated by Django 2.2.5 on 2020-02-20 15:55

from django.db import migrations, models
import nueoffshore.models


class Migration(migrations.Migration):

    dependencies = [
        ('nueoffshore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicants',
            name='cv',
            field=models.FileField(upload_to=nueoffshore.models.user_directory_path, validators=[nueoffshore.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='certification',
            name='certification',
            field=models.FileField(blank=True, upload_to=nueoffshore.models.user_directory_path, validators=[nueoffshore.models.validate_file_extension]),
        ),
    ]