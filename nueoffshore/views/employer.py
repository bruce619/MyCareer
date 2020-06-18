from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from ..forms import CreateJobForm
from ..models import Job, Applicants
from ..filters import ApplicantFilter
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import sweetify
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_datepicker_plus import DateTimePickerInput
from django.core.mail import BadHeaderError
from accounts.models import User
from accounts.decorators import user_is_human_resources
from django.contrib import messages
import datetime
from ..email_task import send_html_mail


class DashboardView(ListView):
    model = Job
    template_name = 'dashboard.html'
    context_object_name = 'jobs'
    ordering = ['-date']
    paginate_by = 2

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_human_resources)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-date')


class ScreenCandidate(FilterView):
    model = Applicants
    template_name = 'screen.html'
    filterset_class = ApplicantFilter
    paginate_by = 2
    ordering = ['id']
    strict = False

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_human_resources)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicants.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the job and pass it as a variable 'job' into the template
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        context['filter'] = ApplicantFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


@login_required(login_url=reverse_lazy('login'))
def filled(request, job_id=None):
    # Gets the the job posted by the logged in user(Admin/HR/Staff)
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    # current date
    now = datetime.datetime.now()
    # check if the job closure
    # Mark as filled
    job.filled = True
    job.save()
    return HttpResponseRedirect(reverse_lazy('employer-dashboard'))


@login_required(login_url=reverse_lazy('login'))
def unfilled(request, job_id=None):
    # Gets the the job posted by the logged in user(Admin/HR/Staff)
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    # Mark as filled
    job.filled = False
    job.save()
    return HttpResponseRedirect(reverse_lazy('employer-dashboard'))


class EmployerCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = CreateJobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('job-listing')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_human_resources)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        users_emails = (User.objects.filter(is_applicant=True).values_list('email', flat=True))
        for user_email in users_emails:
            try:
                context = {}
                send_html_mail(
                    'New Job Position',
                    'CAREERS N.U.E OFFSHORE' + '',
                    user_email,
                    context,
                    "new_job_template.html"
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return super(EmployerCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            sweetify.success(self.request, title='Successfully created job!', text='You have successfully created this job', icon='success', button="OK", timer=3000)
            return self.form_valid(form)
        else:
            sweetify.error(self.request, title='Error', text='Unsuccessful. Kindly try again', icon='error', button='Close', timer=5000)
            return self.form_invalid(form)


# Update a Post
class EmployerUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['title', 'location', 'description', 'requirement', 'years_of_experience', 'type', 'filled', 'end_date']
    template_name = 'job_form.html'
    pk_url_kwarg = 'id'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_human_resources)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        form.fields['end_date'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_human_resources:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, 'Job Detail Updated')
        return reverse_lazy('job-detail', kwargs={'id': self.kwargs['id']})


# Delete a Post
class JobDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('employer-dashboard')
    success_message = 'Job Deleted!!!'

    def test_func(self):
        job = self.get_object()
        # Only HR that created the post are permitted to delete the post
        if self.request.user.is_human_resources:
            return True
        return False

