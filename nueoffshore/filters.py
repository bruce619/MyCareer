import django_filters
from .models import Applicants
from .models import Job


class ApplicantFilter(django_filters.FilterSet):

    class Meta:
        model = Applicants
        fields = ('experience', 'age', 'degree', 'class_of_degree')


class SearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ('title',)
