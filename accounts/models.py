from django.db import models
from django.contrib.auth.models import User
from PIL import Image


SEX_TYPE = (
    ('male', 'Male'),
    ('male', 'Female')
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg')
    sex = models.CharField(choices=SEX_TYPE, blank=True, max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(blank=True, max_length=20)
    Nationality = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

