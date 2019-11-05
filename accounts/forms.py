from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# List of Calender Year
YEARS = [x for x in range(1960, 2020)]


# Form for User Registration
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


# User Update form for Profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


#  Profile Update form for Profile
class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Profile
        fields = ['image', 'sex', 'date_of_birth', 'phone_number', 'Nationality']


