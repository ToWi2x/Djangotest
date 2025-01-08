from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Issue Model (remains unchanged)
class Issues(models.Model):
    TYPE_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    issue_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Hardware')
    description = models.TextField(default='')
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='issues_authored', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_issues', null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')

    def __str__(self):
        return f"{self.issue_type} - {self.description[:30]}"

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})


# Course Model
class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    description = models.TextField(default='open')
    Version = models.TextField(default='Open')

    def __str__(self):
        return f"{self.name} ({self.code})"


# Module Model
class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    credit = models.IntegerField()
    category = models.CharField(max_length=50)
    description = models.TextField(default='open')
    availability = models.BooleanField(default=True)
    courses_allowed = models.ManyToManyField(Course, through='ModuleCoursesAllowed')
    registered = models.ManyToManyField(User, related_name='registered_modules', through='ModuleRegistered')

    def __str__(self):
        return self.name


# ModuleRegistered Model
class ModuleRegistered(models.Model):  
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('module', 'user')  # Prevent multiple registrations for the same module by the same user

    def __str__(self):
        return f"{self.user.username} registered for {self.module.name}"


# ModuleCoursesAllowed Model (through model for the many-to-many relationship)
class ModuleCoursesAllowed(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.module.name} -> {self.course.name}"
    
    
class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you use Django's User model for students
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)  # Automatically sets the registration date to when the record is created

    class Meta:
        unique_together = ('student', 'module')  # Prevents a student from registering for the same module twice

    def __str__(self):
        return f"{self.student.username} registered for {self.module.name} on {self.registration_date}"    
