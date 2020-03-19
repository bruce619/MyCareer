# Generated by Django 2.2.5 on 2020-03-19 15:22

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import nueoffshore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('cv', models.FileField(upload_to=nueoffshore.models.user_directory_path, validators=[nueoffshore.models.validate_file_extension])),
                ('degree', models.CharField(blank=True, choices=[('PhD', 'Doctorate Degree'), ('M.Sc', "Master's Degree"), ('B.Sc', "Bachelor's Degree"), ('HND', 'HND'), ('OND', 'OND'), ('Others', 'Others')], max_length=10)),
                ('class_of_degree', models.CharField(blank=True, choices=[('1st Class', 'First Class'), ('2nd Upper', 'Second Class Upper'), ('2nd lower', 'Second Class Lower'), ('Others', 'Others')], max_length=10)),
                ('age', models.IntegerField(choices=[(18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('location', models.CharField(choices=[('Lagos', 'Lagos State'), ('River', 'Rivers State'), ('Abuja', 'FCT'), ('Delta', 'Delta State'), ('Enugu', 'Enugu State')], max_length=20)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('requirement', ckeditor_uploader.fields.RichTextUploadingField()),
                ('years_of_experience', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(choices=[('Full time', 'Full time'), ('Part time', 'Part time'), ('Internship', 'Internship'), ('Contract', 'Contract')], max_length=10)),
                ('end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('filled', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('certification', models.FileField(blank=True, default='no_certificate.pdf', null=True, upload_to=nueoffshore.models.user_directory_path, validators=[nueoffshore.models.validate_file_extension])),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applicant_certifications', to='nueoffshore.Applicants')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='applicants',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='nueoffshore.Job'),
        ),
        migrations.AddField(
            model_name='applicants',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
