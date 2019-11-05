from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from ..forms import CreateJobForm
from ..models import Job, Applicants
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from bootstrap_datepicker_plus import DateTimePickerInput


class DashboardView(ListView):
    model = Job
    template_name = 'dashboard.html'
    context_object_name = 'jobs'
    ordering = ['-date']
    paginate_by = 2

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-date')


class ApplicantPerJobView(ListView):
    model = Applicants
    template_name = 'applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicants.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the job and pass it as a variable 'job' into the template
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class QualifiedApplicantPerJobView(ListView):
    model = Applicants
    template_name = 'qualified_applicants.html'
    context_object_name = 'applicants'
    paginate_by = 2

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # First we get the job itself by grabbing the job id.
        job = Job.objects.get(id=self.kwargs['job_id'])

        # Add an extra argument to the filter method.
        return Applicants.objects.filter(job=job, experience__gte=job.years_of_experience).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class UnQualifiedApplicantPerJobView(ListView):
    model = Applicants
    template_name = 'unqualified_applicants.html'
    context_object_name = 'applicants'
    paginate_by = 2

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # First we get the job itself by grabbing the job id.
        job = Job.objects.get(id=self.kwargs['job_id'])

        # Add an extra argument to the filter method.
        return Applicants.objects.exclude(job=job, experience__gte=job.years_of_experience).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


@login_required(login_url=reverse_lazy('login'))
def filled(request, job_id=None):
    # Gets the the job posted by the logged in user(Admin/HR/Staff)
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    # When Job is filled mark as filled
    job.filled = True
    job.save()
    return HttpResponseRedirect(reverse_lazy('job-listing'))


class EmployerCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = CreateJobForm
    template_name = 'createjob.html'
    success_url = reverse_lazy('job-listing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the group name and pass it as a variable into the template
        context['in_group'] = self.request.user.groups.filter(name='Human Resources').exists()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EmployerCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(self.request, 'Successfully created job!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# Update a Post
class EmployerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    fields = ['title', 'location', 'description', 'requirement', 'years_of_experience', 'type', 'filled', 'last_date']
    template_name = 'job_form.html'
    pk_url_kwarg = 'id'

    def get_form(self):
        form = super().get_form()
        form.fields['last_date'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('job-detail', kwargs={'id': self.kwargs['id']})


# Delete a Post
class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job-listing')

    def test_func(self):
        job = self.get_object()
        # Only users that created the post are permitted to delete the post
        if self.request.user == job.user:
            return True
        return False


