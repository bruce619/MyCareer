from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError

JOB_TYPE = (
    ('Full time', "Full time"),
    ('Part time', "Part time"),
    ('Internship', "Internship"),
    ('Contract', "Contract"),
)

country_state = (
    ('Lagos', 'Lagos State'),
    ('River', 'Rivers State'),
    ('Abuja', 'FCT'),
    ('Delta', 'Delta State'),
    ('Enugu', 'Enugu State'),
)

DEGREE_TYPE = (
    ('PhD', "Doctorate Degree"),
    ('M.Sc', "Master's Degree"),
    ('B.Sc', "Bachelor's Degree"),
    ('HND', "HND"),
    ('OND', "OND"),
    ('Others', 'Others'),
)

CLASS_OF_DEGREE = (
    ('1st Class', 'First Class'),
    ('2nd Upper', 'Second Class Upper'),
    ('2nd lower', 'Second Class Lower'),
    ('Others', 'Others'),
)


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported! Upload pdf format only')


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
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Applicants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    experience = models.IntegerField(blank=True, null=True)
    cv = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    degree = models.CharField(choices=DEGREE_TYPE, blank=True, max_length=10)
    class_of_degree = models.CharField(choices=CLASS_OF_DEGREE, blank=True, max_length=10)
    age = models.IntegerField(choices=list(zip(range(18, 41), range(18, 41))))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.get_full_name()} Applied'


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applicant_certifications', null=True)
<<<<<<< HEAD
    name = models.CharField(max_length=100)
    certification = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], default='default.pdf')
=======
    name = models.CharField(max_length=50, blank=True, null=True)
    certification = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], blank=True, null=True, default='no_certificate.pdf')
>>>>>>> 6e4227fc5076f65fa6d0c4dc3e3c6e7b1ec310a4

    def __str__(self):
        return f'{self.user.get_full_name(), self.applicant.job, self.name}  certificate'







