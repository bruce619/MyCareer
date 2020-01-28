from django import forms
from .models import Job, Applicants
from bootstrap_datepicker_plus import DateTimePickerInput
import django_filters


class CreateJobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('title', 'location', 'description', 'requirement', 'years_of_experience', 'type', 'last_date')
        exclude = ('user', 'created_at', 'date', 'filled')
        widgets = {
            'last_date': DateTimePickerInput(format='%Y-%m-%d %H:%M')
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
        fields = ('job', 'experience', 'degree', 'cv', 'certification', 'start_date', 'end_date')

