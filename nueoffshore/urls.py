from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.employee import AppliedJobs, job_apply
from .views.employer import DashboardView, EmployerCreateView, EmployerUpdateView,  JobDeleteView, ScreenCandidate, filled
from .views.home import HomeView, SearchView, JobListView, JobDetailView
from django.views.generic import TemplateView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('employer/jobs/create/', EmployerCreateView.as_view(), name='employer-jobs-create'),
    path('jobs/<int:id>/update', EmployerUpdateView.as_view(), name='job-update'),
    path('jobs/job-listing/', JobListView.as_view(), name='job-listing'),
    path('jobs/my-joblist/', AppliedJobs.as_view(), name='my-applied-jobs'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('screen/<int:job_id>', ScreenCandidate.as_view(), name='employer-dashboard-screen'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('jobs/job-detail/<int:id>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('jobs/<int:job_id>/apply', job_apply, name='apply-job'),
    path('successful-apply/', TemplateView.as_view(template_name="success.html"), name="successful-apply"),
    path('job-tips/', TemplateView.as_view(template_name="job_tips.html"), name="job-tips"),
    path('job-benefits/', TemplateView.as_view(template_name="benefits.html"), name="job-benefits"),

]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
