from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from ..forms import ApplyJobForm
from ..models import Applicants, Job
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import sweetify
from django.views.generic import CreateView, ListView
from django.template.loader import get_template
from django.core.mail import EmailMessage


# Apply For a Job
class ApplyJobView(CreateView):
    model = Applicants
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'
    success_url = reverse_lazy('successful-apply')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            sweetify.success(self.request, title='Successfully Applied', text='You have successfully applied for this role', icon='success', button='Close', timer=3000)
            return self.form_valid(form)
        else:
            sweetify.error(self.request, title='Error', text='Application unsuccessful. Kindly re-apply with correct details, ensure the date format is properly entered', icon='error', button='Close', timer=5000)
            return HttpResponseRedirect(reverse_lazy('job-detail', kwargs={'id': self.kwargs['job_id']}))

    def form_valid(self, form):
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
            [#'email'],
        )
        email.content_subtype = 'html'
        form.save()
        email.send()
        return super(ApplyJobView, self).form_valid(form)


# See All Jobs User Applied for
class AppliedJobs(ListView):
    model = Applicants
    template_name = 'my_job_list.html'
    context_object_name = 'applications'
    ordering = ['-date']
    paginate_by = 3

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(applicants__user=user).distinct().order_by('-date')
