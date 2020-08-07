from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import authenticate


# List of Calender Year
YEARS = [x for x in range(1970, 2020)]


# Form for User Registration
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['username'].label = "Username"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_applicant = True
        user.save()
        return user


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password',)
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials")


# User Update form for Profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'username': "Username",
            'email': "Email",
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % account)


#  Profile Update form for Profile
class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Profile
        fields = ('image', 'sex', 'birth_date', 'phone_number', 'nationality',)
        labels = {
            'image': "Image",
            'sex': "Sex",
            'birth_date': "Date Of Birth",
            'phone_number': "Phone Number",
            'nationality': "Nationality",
        }
        widgets = {
            'last_name': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'nationality': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean_phonenumber(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
        except User.DoesNotExist:
            return phone_number
        raise forms.ValidationError('Phone Number "%s" is already in use.' % account)


