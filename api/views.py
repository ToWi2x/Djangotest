from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # Allow read-only access to unauthenticated users
from itreporting.models import Issues
from .serializers import IssueSerializer
from .permissions import IsAuthorOrReadOnly

class IssueViewSet(ModelViewSet):
    queryset = Issues.objects.all().order_by('date_submitted')
    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set both `author` and `reported_by` fields to the logged-in user
        serializer.save(author=self.request.user, reported_by=self.request.user)
