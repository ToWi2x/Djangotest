from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Module, Issues, Registration
from django.core.mail import send_mail
from users.forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin  # Ensures the user is logged in for certain views
from users.forms import IssueForm  # Import the form from the users folder
from django.http import HttpResponseRedirect
import requests

# Home view
def home(request):
    # API URL and cities for weather data
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = 'c270eba7498956b83993992478ae0a69'  # Your actual API key

    # Fetch weather data for each city
    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json()
        print(city_weather)  # Check the API response in the terminal
        if city_weather.get('cod') == 200:  # Ensure valid response
            weather = {
                'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description']
            }
            weather_data.append(weather)

    # Fetch courses and modules
    courses = Course.objects.all()
    modules = Module.objects.all()

    # Combine data in the context
    return render(request, 'itreporting/home.html', {
        'title': 'Homepage',
        'weather_data': weather_data,  # Weather information for each city
        'courses': courses,  # List of courses
        'modules': modules  # List of modules
    })

# About view
def about(request):
    return render(request, 'itreporting/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, email, [settings.CONTACT_EMAIL], fail_silently=False)
            return redirect('itreporting:contact_success')
    else:
        form = ContactForm()
    return render(request, 'itreporting/contact.html', {'form': form})


# Success page after contact form submission
def contact_success(request):
    return render(request, 'itreporting/contact_success.html')

# Report view displaying all issues
def report(request):
    daily_report = {'issues': Issues.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def modules_list(request):
    # Get all modules, ensuring courses are loaded
    modules = Module.objects.prefetch_related('courses_allowed').all()

    return render(request, 'itreporting/modules_list.html', {'modules': modules})

# Handle module registration/unregistration

@login_required
def module_page(request, module_id):
    # Get the module by ID
    module = get_object_or_404(Module, id=module_id)
    
    # Handle registration/unregistration via POST request
    if request.method == 'POST':
        # Check if the user is already registered for the module
        if request.user in module.registered.all():
            # Unregister user
            module.registered.remove(request.user)  # Remove from module
            # Also remove the corresponding Registration entry
            Registration.objects.filter(student=request.user, module=module).delete()  # Delete the Registration record
            messages.success(request, "Successfully unregistered from the module.")
        else:
            # Register user if module is available
            if module.availability:
                module.registered.add(request.user)  # Add user to module
                # Create the corresponding Registration object
                Registration.objects.create(student=request.user, module=module)  # Create the Registration record
                messages.success(request, "Successfully registered for the module.")
            else:
                messages.error(request, "This module is not available for registration.")
    
    # Pass the module and its associated data to the template
    return render(request, 'itreporting/modules.html', {
        'module': module,
        'courses_allowed': module.courses_allowed.all(),  # List of courses linked to this module
        'modules': Module.objects.all()  # To display all modules in the list
    })


@login_required
def course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(courses_allowed=course)

    # Handle registration and unregistration
    if request.method == "POST":
        module_id = request.POST.get("module_id")
        action = request.POST.get("action")
        module = get_object_or_404(Module, id=module_id)

        if action == "register":
            module.registered.add(request.user)
        elif action == "unregister":
            module.registered.remove(request.user)

        # Redirect to the same page after processing the form
        return HttpResponseRedirect(request.path_info)

    # Get IDs of modules the user is registered to
    registered_module_ids = request.user.registered_modules.values_list('id', flat=True)

    return render(request, 'itreporting/course_page.html', {
        'course': course,
        'modules': modules,
        'registered_module_ids': registered_module_ids,
    })

# Class-based views for Issues

class PostListView(ListView):
    model = Issues
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10

    def get_queryset(self):
        return Issues.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Initialize paginator instance
        paginator = Paginator(context['issues'], self.paginate_by)
        page = self.request.GET.get('page')  # Get the page number from the query string
        issues = paginator.get_page(page)  # Get the issues for the current page
        
        # Add the paginated issues to the context
        context['page_obj'] = issues
        return context

class PostDetailView(DetailView):
    model = Issues
    template_name = 'itreporting/issue_detail.html'
    context_object_name = 'issue'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issues
    template_name = 'itreporting/issue_form.html'
    fields = ['issue_type', 'description', 'room', 'urgent', 'priority', 'status', 'assigned_to']
    success_url = reverse_lazy('itreporting:report')

    def form_valid(self, form):
        # Automatically set the logged-in user as the author and reported_by
        form.instance.author = self.request.user
        form.instance.reported_by = self.request.user  # Ensure reported_by is set
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Issues
    template_name = 'itreporting/issue_confirm_delete.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('itreporting:report')  # Redirect after successful deletion

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Issues
    template_name = 'itreporting/issue_form.html'  
    fields = ['issue_type', 'description', 'room', 'urgent', 'priority', 'status', 'assigned_to']  # Fields to be updated
    success_url = reverse_lazy('itreporting:report')  # Redirect to the report page after successful update
