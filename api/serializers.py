from rest_framework.serializers import ModelSerializer, ReadOnlyField
from itreporting.models import Issues

class IssueSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')  # Display the username of the author
    reported_by = ReadOnlyField(source='reported_by.username')  # Display the username of the user reporting the issue

    class Meta:
        model = Issues
        fields = ['issue_type', 'description', 'room', 'urgent', 'date_submitted', 'author', 'assigned_to', 'priority', 'status', 'reported_by']
