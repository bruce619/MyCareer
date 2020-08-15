from django.db import models
from PIL import Image
from django.core.files.storage import default_storage as storage
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from nueoffshore.extra import ContentTypeRestrictedFileField
from django.core.exceptions import ValidationError


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=15, unique=True, blank=False, error_messages={
                                  'unique': "Username already exists.",
                              })
    email = models.EmailField(verbose_name='email', max_length=60, unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    datetimecreated = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_human_resources = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __unicode__(self):
        return self.email

    objects = MyAccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# Choice Selection for Users Gender
SEX_TYPE = (
    ('male', 'Male'),
    ('male', 'Female')
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpeg', '.jpg', '.png']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported! Upload image format only')


#  Profile Model: Will be saved the the database
class Profile(models.Model):
    # Columns for Profile Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(verbose_name="Image", upload_to=user_directory_path, default='default.jpg')
    image = ContentTypeRestrictedFileField(
        upload_to=user_directory_path,
        content_types=['image/jpeg'],
        max_upload_size=20971520,
        default='default.jpg',
        validators=[validate_file_extension]
        )
    sex = models.CharField(verbose_name="Sex", choices=SEX_TYPE, null=True, blank=True, max_length=10)
    birth_date = models.DateField(verbose_name="Date Of Birth", null=True, blank=True)
    phone_number = models.CharField(verbose_name="phone number", max_length=20, unique=True, null=True, blank=True,
                                    error_messages={
                                       'unique': "Phone number already exists.",
                                    })
    nationality = models.CharField(verbose_name="Nationality", null=True, blank=True, max_length=20)

    def __str__(self):
        #  Return the username on the database "e.g Anderson Dean Profile"
        return "{} {} Profile".format(self.user.first_name, self.user.last_name)

    # Saves a users profile
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size, Image.ANTIALIAS)
            fh = storage.open(self.image.name, "w")
            ext = 'jpeg'
            format = 'JPEG' if ext.lower() == 'jpg' else ext.upper()
            img.save(fh, format)
            fh.close()

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

