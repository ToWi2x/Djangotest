from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('report/', PostListView.as_view(), name='report'),  # List all issues
    path('issues/<int:pk>/', PostDetailView.as_view(), name='issue-detail'),  # View details of an issue
    path('issues/new/', PostCreateView.as_view(), name='issue-create'),  # Create a new issue
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name='issue-update'),  # Update an issue
    path('issues/<int:pk>/delete/', PostDeleteView.as_view(), name='issue-delete'),  # Delete an issue
 
    # Module URLs
    path('modules/', views.modules_list, name='modules_list'),  # List all modules
    path('modules/<int:module_id>/', views.module_page, name='module_page'),  # View specific module
    
    # User authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Contact success URL
    path('contact-success/', views.contact_success, name='contact_success'),
    path('course/<int:course_id>/', views.course_page, name='course_page'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)