from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from ..forms import ApplyJobForm
from ..models import Applicants, Job
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView


# Apply For a Job
class ApplyJobView(CreateView):
    model = Applicants
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(self.request, 'Successfully applied for this job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

    def get_success_url(self):
        return reverse_lazy('job-detail', kwargs={'id': self.kwargs['job_id']})

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicants.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # Get users full name, job role applied for, and pass it into an email and save user.
        form.instance.user = self.request.user
        fullname = self.request.user.get_full_name()
        job = Job.objects.get(id=self.kwargs['job_id'])
        template = get_template('applicants_template.html')
        context = {
            'fullname': fullname,
            'job': job,
        }
        content = template.render(context)
        email = EmailMessage(
            "New applicant form submission",
            content,
            'CAREERS N.U.E OFFSHORE' + '',
            ['chimuanya.ibecheozor@nueoffshore.com'],
        )
        email.content_subtype = 'html'
        email.send()
        form.save()
        return super().form_valid(form)


