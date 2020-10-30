import django_filters as df
from .models import Trace


class TraceFilter(df.FilterSet):
    class Meta:
        model = Trace
        fields = {
            'user_id': ['exact'],
            'date': ['exact'],
            'lng_upper_limit': ['lte', 'gte'],
            'lng_lower_limit': ['lte', 'gte'],
            'lat_upper_limit': ['lte', 'gte'],
            'lat_lower_limit': ['lte', 'gte'],
        }
