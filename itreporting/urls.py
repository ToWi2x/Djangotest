from django.urls import path
from .import views
from .views import PostListView, PostDetailView
from .views import PostListView, PostDetailView, PostCreateView,PostUpdateView
from .views import PostListView, PostDetailView, PostCreateView,PostUpdateView, PostDeleteView

app_name = 'itreporting'

urlpatterns = [
path('', views.home, name = 'home'),
path('about/', views.about, name = 'about'),
path('contact/', views.contact, name = 'contact'),
path('report/', PostListView.as_view(), name = 'report'),
path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issues-update'),
path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issues-delete'),
]


