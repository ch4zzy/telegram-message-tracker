import django_filters
from tracker.models import SourceChannel

class SourceChannelFilter(django_filters.FilterSet):
    class Meta:
        model = SourceChannel
        fields = ['source_link']