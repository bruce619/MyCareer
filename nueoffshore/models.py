from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

DEGREE_TYPE = (
    ('B.Sc', "Bachelor's Degree"),
    ('M.Sc', "Master's Degree"),
    ('PhD', "Doctorate Degree"),
)

JOB_TYPE = (
    ('Full time', "Full time"),
    ('Part time', "Part time"),
    ('Internship', "Internship"),
    ('Contract', "Contract"),
)

country_state = (
    ('Lagos', 'Lagos State'),
    ('Rivers', 'Rivers State'),
    ('Abuja', 'FCT'),
    ('Delta', 'Delta State'),
    ('Enugu', 'Enugu State'),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(choices=country_state, max_length=20)
    description = RichTextUploadingField()
    requirement = RichTextUploadingField()
    years_of_experience = models.IntegerField(blank=True, null=True)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    last_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Applicants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    experience = models.IntegerField(blank=True, null=True)
    cv = models.FileField(upload_to=user_directory_path)
    certification = models.FileField(upload_to=user_directory_path, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    degree = models.CharField(choices=DEGREE_TYPE, blank=True, max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.get_full_name()} Applied'

