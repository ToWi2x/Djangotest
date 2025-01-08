from django.contrib import admin
from .models import Issues, Course, Module, ModuleCoursesAllowed, Registration

# Register the Issues model
admin.site.register(Issues)  # Keep this simple for the Issues model

# Register the Registration model with a custom admin interface for better visibility
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'registration_date')  # Display student, module, and registration date
    search_fields = ('student__username', 'module__name')  # Allow search by student or module name
    list_filter = ('module',)  # Filter by module
    ordering = ('-registration_date',)  # Order by registration date (newest first)

# Inline configuration for linking Modules to Courses
class ModuleCoursesAllowedInline(admin.TabularInline):
    model = ModuleCoursesAllowed
    extra = 1  # Number of blank rows to display for adding new links

# Admin configuration for Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [ModuleCoursesAllowedInline]  # Include the inline to manage course links
    list_display = ('name', 'code', 'credit', 'category', 'availability')
    search_fields = ('name', 'code')

# Admin configuration for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleCoursesAllowedInline]  # Include the inline to manage module links
    list_display = ('name', 'code', 'description', 'Version')
    search_fields = ('name', 'code')

# Admin configuration for ModuleCoursesAllowed
@admin.register(ModuleCoursesAllowed)
class ModuleCoursesAllowedAdmin(admin.ModelAdmin):
    list_display = ('module', 'course')  # Show the module and course relationships
    list_filter = ('course', 'module')  # Add filters for easy navigation
    search_fields = ('module__name', 'course__name')  # Allow searching by module or course name
