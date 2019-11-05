from ..models import Job
from django.views.generic import ListView, DetailView


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]


class SearchView(ListView):
    model = Job
    template_name = 'search.html'
    context_object_name = 'jobs'

    #  Query the database for letters similar to the search
    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['title'])


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













