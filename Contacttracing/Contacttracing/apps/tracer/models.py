from django.db import models

from mew.core.models import BaseModel


class Trace(BaseModel):
    user_id = models.IntegerField(default=0)
    lng_upper_limit = models.FloatField()
    lng_lower_limit = models.FloatField()
    lat_upper_limit = models.FloatField()
    lat_lower_limit = models.FloatField()
    trace_file_url = models.CharField(max_length=512, default="")
