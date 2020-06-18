from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from ..forms import ApplyJobForm, ApplyFormset
from ..models import Applicants, Job, Certification
from django.contrib.auth.mixins import LoginRequiredMixin
import sweetify
from django.views.generic import ListView
from django.core.mail import BadHeaderError
from accounts.models import User
from django.contrib.auth.decorators import login_required
from ..email_task import send_html_mail


@login_required(login_url=reverse_lazy('login'))
def job_apply(request, job_id=None):
    template_name = 'apply_form.html'
    applyform = ApplyJobForm(request.GET or None)
    job = Job.objects.get(id=job_id)
    formset = ApplyFormset(queryset=Certification.objects.none())
    if request.method == 'GET':
        context = {'applyform': applyform, 'formset': formset}
        return render(request, template_name, context)
    elif request.method == 'POST':
        applyform = ApplyJobForm(request.POST, request.FILES)
        formset = ApplyFormset(request.POST, request.FILES)
        if applyform.is_valid() and formset.is_valid():
            applyform.instance.user = request.user
            apply = applyform.save(commit=False)
            apply.job = job
            apply.save()
            for form in formset:
                # so that `apply` instance can be attached.
                certification = form.save(commit=False)
                certification.user = request.user
                certification.applicant = apply
                certification.save()
            first_name = request.user.first_name
            last_name = request.user.last_name
            hr_email = (User.objects.filter(is_human_resources=True).values_list('email', flat=True))
            applicants_email = (User.objects.filter(is_applicant=True).values_list('email', flat=True))
            for h_mail in hr_email:
                try:
                    context = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'job': job,
                        }
                    send_html_mail(
                        'New applicant form submission',
                        'CAREERS N.U.E OFFSHORE' + '',
                        h_mail,
                        context,
                        "applicants_template.html"
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            for a_mail in applicants_email:
                try:
                    context = {
                            'job': job,
                        }
                    send_html_mail(
                        'Application Successful',
                        'CAREERS N.U.E OFFSHORE' + '',
                        a_mail,
                        context,
                        "application_successful.html"
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            sweetify.success(request, title='Successful Application', text='You have successfully applied for {}'.format(job), icon='success', button="OK", timer=3000)
            return redirect('successful-apply')

    return render(request, template_name, {'applyform': applyform, 'formset': formset})


# See All Jobs User Applied for
class AppliedJobs(ListView, LoginRequiredMixin):
    model = Applicants
    template_name = 'my_job_list.html'
    context_object_name = 'applications'
    ordering = ['-date']
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(applicants__user=user).distinct().order_by('-date')