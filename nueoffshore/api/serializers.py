from rest_framework import serializers
from ..models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'description', 'requirement', 'years_of_experience',
                  'type', 'end_date', 'created_at', 'date', 'filled']
        read_only_fields = ('id', 'user', 'date', 'created_at',)


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = ['id', 'user', 'job', 'experience', 'cv', 'degree', 'class_of_degree', 'age', 'created_at']
        read_only_fields = ('id', 'user', 'job', 'created_at',)


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'user', 'applicant', 'name', 'certification']
        read_only_fields = ('id', 'applicant',)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        models = Notification
        fields = ['id', 'sender', 'receiver', 'job', 'message', 'message_sent', 'message_seen', 'dateTimeCreated']
        read_only_fields = ('id', 'job', 'dateTimeCreated',)