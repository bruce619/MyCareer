import django_filters
from .models import Applicants
from .models import Job


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
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ('title',)
