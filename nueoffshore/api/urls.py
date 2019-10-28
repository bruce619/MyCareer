from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('jobs/job-listing/', JobViewSet, base_name='job-listing')

urlpatterns = [
    path('search/', SearchApiView.as_view()),
    path('apply-job/<int:job_id>', ApplyJobApiView.as_view())
]

urlpatterns += router.urls
