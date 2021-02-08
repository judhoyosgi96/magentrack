from django.db import models

class Variable(models.Model):
    """Variable class"""
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=15, null=False, blank=False, unique=True)
    value = models.CharField(max_length=3,null=False)
    class Meta:
        unique_together = ('id','name',)