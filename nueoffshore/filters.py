import django_filters
from .models import Applicants
from .models import Job, Notification
from django.db.models import Q
from functools import reduce
import operator


class MyRangeWidget(django_filters.widgets.RangeWidget):

    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class ApplicantFilter(django_filters.FilterSet):
    experience = django_filters.RangeFilter(label='Experience',
                                            widget=MyRangeWidget(
                                                from_attrs={'placeholder': 'from'},
                                                to_attrs={'placeholder': 'to'},
                                            )
                                            )
    age = django_filters.RangeFilter(label='Age',
                                     widget=MyRangeWidget(
                                        from_attrs={'placeholder': 'from'},
                                        to_attrs={'placeholder': 'to'},
                                            )
                                     )

    class Meta:
        model = Applicants
        fields = ('experience', 'age', 'degree', 'class_of_degree')


class SearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="Job Title")

    class Meta:
        model = Job
        fields = ('title',)


class InboxSearchFilter(django_filters.FilterSet):
    multi_name_fields = django_filters.CharFilter(method='filter_by_all_name_fields')

    class Meta:
        model = Notification
        fields = ()

    def filter_by_all_name_fields(self, queryset, name, value):

        """
        Split the filter value into separate search terms and construct a set of queries from this.
        The set of queries includes an icontains lookup for the lookup fields for each of the search terms.
        The set of queries is then joined
        with the OR operator.
        """

        lookups = ['sender__first_name__icontains', 'sender__last_name__icontains', 'job__title__icontains']

        or_queries = [Q(**{lookup: value}) for lookup in lookups]

        return queryset.filter(reduce(operator.or_, or_queries))


class SentSearchFilter(django_filters.FilterSet):
    multi_name_fields = django_filters.CharFilter(method='filter_by_all_name_fields', label='search')

    class Meta:
        model = Notification
        fields = ['multi_name_fields']

    def filter_by_all_name_fields(self, queryset, name, value):

        """
                Split the filter value into separate search terms and construct a set of queries from this.
                The set of queries includes an icontains lookup for the lookup fields for each of the search terms.
                The set of queries is then joined
                with the OR operator.
                """

        lookups = ['receiver__first_name__icontains', 'receiver__last_name__icontains', 'job__title__icontains']

        or_queries = [Q(**{lookup: value}) for lookup in lookups]

        return queryset.filter(reduce(operator.or_, or_queries))


# Q(sender__first_name__contains=self.request.GET.get('receiver', False))