from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import *
from ..models import Job, Applicants, Certification, Notification


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_create_job_api_view(request):

    try:
        jobs = Job.objects.all().order_by("-created_at")
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(jobs, many=True)
        return JsonResponse({'jobs': serializer.data}, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        user = request.user.is_human_resources
        job = Job(user=user)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'job': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_apply_job_api_view(request, job_id=None):

    user = request.user.id
    an_applicant = request.user.is_applicant

    try:
        my_jobs = Job.objects.filter(applicants__user=user).distinct().order_by("-created_at")
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(my_jobs, many=True)
        return JsonResponse({'jobs': serializer.data}, safe=False, status=status.HTTP_200_OK)

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not an_applicant:
        return Response({'Response': 'You do not have the permission to apply'})

    if request.method == 'POST':
        jobs = Applicants(user=user, job=job)
        serializer = JobSerializer(jobs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'jobs': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




# class JobViewSet(generics.ListAPIView):
#     serializer_class = JobSerializer
#     queryset = serializer_class.Meta.model.objects.all()
#     permission_classes = [IsAuthenticated]
#
#
# class SearchApiView(generics.ListAPIView):
#     serializer_class = JobSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return self.serializer_class.Meta.model.objects.filter(title__contains=self.request.GET['title'])
#
#
# class ApplyJobApiView(generics.ListCreateAPIView):
#     serializer_class = ApplicantSerializer
#     http_method_names = [u'post']
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
