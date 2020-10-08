import django_filters as df
from .models import Trace


class TraceFilter(df.FilterSet):
    class Meta:
        model = Trace
