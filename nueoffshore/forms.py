from django import forms
from .models import Job, Applicants, Certification, Notification
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import modelformset_factory


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


class CreateJobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CreateJobForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['end_date'].required = True

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
        job.save()
        return job


class ApplyJobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ApplyJobForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['degree'].required = True
        self.fields['class_of_degree'].required = True
        self.fields['experience'].required = True
        self.fields['age'].required = True
        self.fields['cv'].required = True

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


class NotificationForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Your Message',
            }
        )

    class Meta:
        model = Notification
        fields = ('sender', 'receiver', 'job', 'message', 'message_sent', 'dateTimeCreated',)
        exclude = ('sender', 'receiver', 'job', 'message_sent', 'dateTimeCreated',)
