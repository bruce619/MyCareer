from django.db import models
from django.utils import timezone
from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.conf import settings
from .extra import ContentTypeRestrictedFileField


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
    ('PhD', "PhD"),
    ('Mphil', "Mphil"),
    ('M.Sc', "M.Sc"),
    ('MBA', "MBA"),
    ('MBBS', "MBBS"),
    ('B.Sc', "B.Sc"),
    ('HND', "HND"),
    ('OND', "OND"),
    ('Diploma', "Diploma"),
    ('NCE', "NCE"),
    ('SSCE/WAEC', "SSCE/WAEC"),
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
    end_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Applicants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    experience = models.IntegerField(blank=True, null=True)
    cv = ContentTypeRestrictedFileField(
        upload_to=user_directory_path,
        content_types=['application/pdf'],
        max_upload_size=20971520,
        validators=[validate_file_extension]
    )
    # cv = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    degree = models.CharField(choices=DEGREE_TYPE, blank=True, max_length=10)
    class_of_degree = models.CharField(choices=CLASS_OF_DEGREE, blank=True, max_length=10)
    age = models.IntegerField(choices=list(zip(range(18, 41), range(18, 41))))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} Applied".format(self.user.first_name, self.user.last_name)


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applicant_certifications', null=True)
    name = models.CharField(max_length=100, default='None')
    # certification = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], default='default.pdf')
    certification = ContentTypeRestrictedFileField(
        upload_to=user_directory_path,
        content_types=['application/pdf', 'application/zip'],
        max_upload_size=20971520,
        default='default.pdf',
        validators=[validate_file_extension]
    )

    def __str__(self):
        return "{} {} {} Certificate".format(self.user.first_name, self.user.last_name, self.name)


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    job = models.ForeignKey(Job, verbose_name="Job id", on_delete=models.CASCADE)
    message = models.TextField(max_length=None)
    message_sent = models.BooleanField(default=False)
    message_seen = models.BooleanField(default=False)
    dateTimeCreated = models.DateTimeField(verbose_name='sent_date', auto_now_add=True)

    def __str__(self):
        return str(self.sender) + " to " + str(self.receiver)