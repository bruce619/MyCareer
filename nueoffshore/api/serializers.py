from rest_framework import serializers

from nueoffshore.models import Job, Applicants


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = "__all__"
