from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.employee import ApplyJobView
from .views.employer import DashboardView, EmployerCreateView, EmployerUpdateView,  JobDeleteView, ApplicantPerJobView, \
                            QualifiedApplicantPerJobView, UnQualifiedApplicantPerJobView, filled
from .views.home import HomeView, SearchView, JobListView, JobDetailView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('employer/jobs/create/', EmployerCreateView.as_view(), name='employer-jobs-create'),
    path('jobs/<int:id>/update', EmployerUpdateView.as_view(), name='job-update'),
    path('jobs/job-listing/', JobListView.as_view(), name='job-listing'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('qualified-applicants/<int:job_id>', QualifiedApplicantPerJobView.as_view(), name='employer-dashboard-qualified-applicants'),
        path('unqualified-applicants/<int:job_id>', UnQualifiedApplicantPerJobView.as_view(), name='employer-dashboard-unqualified-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('jobs/job-detail/<int:id>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),


]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
