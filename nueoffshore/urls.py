from django.urls import path, include
from .views.employee import *
from .views.employer import *
from .views.home import *
from django.views.generic import TemplateView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('employer/jobs/create/', EmployerCreateView.as_view(), name='employer-jobs-create'),
    path('jobs/job-listing/', JobListView.as_view(), name='job-listing'),
    path('jobs/job-detail/<int:id>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/job-detail/<int:id>/update', EmployerUpdateView.as_view(), name='job-update'),
    path('jobs/job-detail/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('jobs/my-joblist/', AppliedJobs.as_view(), name='my-applied-jobs'),
    path('employer/dashboard/', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('screen/<int:job_id>/', ScreenCandidate.as_view(), name='employer-dashboard-screen'),
        path('mark-filled/<int:job_id>/', filled, name='job-mark-filled'),
        path('unmark-filled/<int:job_id>/', unfilled, name='job-unmark-filled'),
    ])),
    path('jobs/<int:job_id>/apply/', job_apply, name='apply-job'),
    path('send-notification/<int:job_id>/<int:applicant_id>', send_notification, name='send-notification'),
    path('reply-notification/<int:id>/', reply_message, name='reply-notification'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentView.as_view(), name='sent'),
    path('mark-as-read/<int:id>/', mark_as_read, name='mark-as-read'),
    path('delete-message/<int:pk>/', DeleteMessage.as_view(), name='delete-message'),
    path('successful-apply/', TemplateView.as_view(template_name="success.html"), name="successful-apply"),
    path('job-tips/', TemplateView.as_view(template_name="job_tips.html"), name="job-tips"),
    path('job-benefits/', TemplateView.as_view(template_name="benefits.html"), name="job-benefits"),

]

