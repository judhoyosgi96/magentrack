from django.db import models
from django.contrib.gis.db import models

from apps.dataset.models import Dataset

class Row(models.Model):
    """Row class"""
    dataset_id = models.ForeignKey(Dataset, null=False, on_delete=models.CASCADE)
    point = models.PointField(geography=True, null=True)
    client_id = models.IntegerField(null=True)
    client_name = models.CharField(max_length=45, null=True)
