from django import forms
from .models import Job, Applicants, Certification
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import modelformset_factory

DEGREE_TYPE = (
    ('PhD', "Doctorate Degree"),
    ('M.Sc', "Master's Degree"),
    ('B.Sc', "Bachelor's Degree"),
    ('HND', "HND"),
    ('OND', "OND"),
    ('Others', 'Others'),
)


class CreateJobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('title', 'location', 'description', 'requirement', 'years_of_experience', 'type', 'end_date')
        exclude = ('user', 'created_at', 'date', 'filled')
        widgets = {
            'end_date': DateTimePickerInput(format='%Y-%m-%d %H:%M')
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class ApplyJobForm(forms.ModelForm):

    class Meta:
        model = Applicants
        fields = ('job', 'degree', 'class_of_degree', 'experience', 'age', 'cv')
        exclude = ('job',)
        labels = {
            'degree': 'Degree',
            'class_of_degree': 'Class Of Degree',
            'experience': 'Years of Experience',
            'age': 'Age',
            'cv': 'CV',

        }
        widgets = {
            'degree': forms.Select(attrs={
                'class': 'form-control',
            }
            ),
            'class_of_degree': forms.Select(attrs={
                'class': 'form-control',
            }
            ),
            'experience': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'age': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'cv': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


ApplyFormset = modelformset_factory(
    Certification,
    fields=('name', 'certification'),
    extra=1,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Document name'
            }
        ),
        'certification': forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Document'
            }
        )
    }
)

