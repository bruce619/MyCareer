from ..models import Job, Applicants, Notification
from ..forms import NotificationForm
from django.views.generic import ListView, DetailView, DeleteView
from accounts.forms import ProfileUpdateForm
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ..filters import SearchFilter, InboxSearchFilter, SentSearchFilter
from django_filters.views import FilterView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError
from ..email_task import send_html_mail


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'
    form_class = ProfileUpdateForm

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(FilterView):
    model = Job
    template_name = 'search.html'
    filterset_class = SearchFilter
    ordering = ['-date']
    paginate_by = 3
    context_object_name = 'jobs'
    strict = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class JobListView(ListView):
    model = Job
    template_name = 'job_listing.html'
    context_object_name = 'jobs'
    ordering = ['-date']
    paginate_by = 4


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'


def send_notification(request, job_id=None, applicant_id=None):
    template_name = 'send_notification.html'
    form = NotificationForm(request.GET or None)
    applicant = get_object_or_404(Applicants, id=applicant_id)
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            try:
                datetimecreated = timezone.now()
                receiver = applicant.user
                title = job

                notification = Notification()
                notification.sender = request.user
                notification.receiver = receiver
                notification.job = title
                notification.message = message
                notification.message_sent = True
                notification.dateTimeCreated = datetimecreated
                notification.save()

                try:
                    receiver_email = str(applicant.user.email)
                    print(receiver_email)
                    context = {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'job': job.title
                    }
                    send_html_mail(
                        "New Message",
                        'CAREERS N.U.E OFFSHORE' + '',
                        [receiver_email],
                        context,
                        "notification_template.html"
                    )

                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                messages.success(request, "Your message has been sent.")
                return redirect("home")

            except ObjectDoesNotExist:
                messages.warning(request, "Message not sent")
                return redirect("employer-dashboard-screen", id=job_id)

    return render(request, template_name, {form: 'form'})


def reply_message(request, id=None):
    template_name = 'send_notification.html'
    form = NotificationForm(request.GET or None)
    notification = get_object_or_404(Notification, id=id)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            try:
                datetimecreated = timezone.now()
                receiver = notification.sender
                print(receiver)
                title = notification.job.title

                notification = Notification()
                notification.sender = request.user
                notification.receiver = receiver
                notification.job = Job.objects.get(title=title)
                notification.message = message
                notification.message_sent = True
                notification.dateTimeCreated = datetimecreated
                notification.save()

                try:
                    receiver_email = str(receiver)
                    context = {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'job': Job.objects.get(title=title)
                    }
                    send_html_mail(
                        "New Message",
                        'CAREERS N.U.E OFFSHORE' + '',
                        [receiver_email],
                        context,
                        "notification_template.html"
                    )

                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                messages.success(request, "Your message has been sent.")
                return redirect("inbox")

            except ObjectDoesNotExist:
                messages.warning(request, "Message not sent")
                return redirect("reply-notification", id=id)

    return render(request, template_name, {form: 'form'})


def mark_as_read(request, id=None):
    notification = get_object_or_404(Notification, id=id)
    notification.message_seen = True
    notification.save()
    return redirect('inbox')


class DeleteMessage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Notification
    template_name = 'notification_confirm_delete.html'
    success_url = reverse_lazy('inbox')
    success_message = 'successfully deleted!'


class InboxView(FilterView):
    model = Notification
    template_name = 'inbox.html'
    filterset_class = InboxSearchFilter
    ordering = ['-dateTimeCreated']
    paginate_by = 7
    strict = False

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = InboxSearchFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(receiver=user).distinct().order_by('-dateTimeCreated')


class SentView(ListView):
    model = Notification
    template_name = 'sent.html'
    filterset_class = SentSearchFilter
    ordering = ['-dateTimeCreated']
    paginate_by = 7
    strict = False

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SentSearchFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(sender=user).distinct().order_by('-dateTimeCreated')


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)








