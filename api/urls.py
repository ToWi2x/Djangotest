from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueViewSet
from rest_framework.authtoken.views import obtain_auth_token 

# Create a router object to automatically handle URL patterns
router = DefaultRouter()
router.register(r'issues', IssueViewSet)  # Register the IssueViewSet with the path "issues/"

# Define the urlpatterns for the API
urlpatterns = [
    path('', include(router.urls)),  # Include all routes registered with the router
    path('api/auth/', obtain_auth_token, name='api_token_auth'),

]
