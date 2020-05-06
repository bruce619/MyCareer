from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage as storage


# Choice Selection for Users Gender
SEX_TYPE = (
    ('male', 'Male'),
    ('male', 'Female')
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


#  Profile Model: Will be saved the the database
class Profile(models.Model):
    # Columns for Profile Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg')
    sex = models.CharField(choices=SEX_TYPE, null=True, blank=True, max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=20)
    Nationality = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        #  Return the username on the database "e.g Dean Profile"
        return f'{self.user.username} Profile'

    # Saves a users profile
    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size, Image.ANTIALIAS)
    #         fh = storage.open(self.image.name, "w")
    #         ext = 'jpeg'
    #         format = 'JPEG' if ext.lower() == 'jpg' else ext.upper()
    #         img.save(fh, format)
    #         fh.close()

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

