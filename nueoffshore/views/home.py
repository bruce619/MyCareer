from ..models import Job
from django.views.generic import ListView, DetailView
from accounts.forms import ProfileUpdateForm
from django.shortcuts import render
from django.utils import timezone
from ..filters import SearchFilter
from django_filters.views import FilterView


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'
    form_class = ProfileUpdateForm

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(FilterView):
    model = Job
    template_name = 'search.html'
    filterset_class = SearchFilter
    ordering = ['-date']
    paginate_by = 3
    context_object_name = 'jobs'
    strict = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class JobListView(ListView):
    model = Job
    template_name = 'job_listing.html'
    context_object_name = 'jobs'
    ordering = ['-date']
    paginate_by = 4


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_group'] = self.request.user.groups.filter(name='Applicants').exists()
        return context


def error_404(request):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)








