from django.db import models

class Dataset(models.Model):
    """Dataset class"""
    name = models.CharField(max_length=95, null=False)
    date = models.DateField(null=False)