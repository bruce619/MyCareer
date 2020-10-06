from django.urls import path
from rest_framework.routers import format_suffix_patterns
from .views import *

urlpatterns = [
    path('jobs/', get_create_job_api_view, name="job-listing"),
    path('job-apply/', get_apply_job_api_view, name='job-apply')
]

urlpatterns = format_suffix_patterns(urlpatterns)
