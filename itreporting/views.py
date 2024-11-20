from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issues
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.views.generic.edit import DeleteView
def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

# Create your views here.
def about(request):
    return HttpResponse('<h1> Welcome to about</h1>')

def contact(request):
     return HttpResponse('<h1> Welcome to contact</h1>')
 

def report(request):
    daily_report = {'issues': Issues.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

class PostListView(ListView):
    model = Issues
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10  # Optional pagination
    
class PostDetailView(DetailView):
    model = Issues
    template_name = 'itreporting/issue_detail.html'
    
class PostListView(ListView):
    model = Issues
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10 # Optional pagination
    
class PostDetailView(DetailView):
    model = Issues
    template_name = 'itreporting/issue_detail.html'
    
class PostCreateView(CreateView):

    model = Issues
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form): 

        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Issues
    fields = ['type', 'room', 'details']
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 

    model = Issues

    fields = ['type', 'room', 'details']
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issues
    success_url = '/report'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Issues

    success_url = '/report'
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author
    
class PostListView(ListView):
    model = Issues
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5  # Optional pagination

