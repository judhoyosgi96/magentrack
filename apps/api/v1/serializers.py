from rest_framework import serializers

from django.core.validators import FileExtensionValidator
from apps.dataset.models import Dataset

class DatasetSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=95)
    file=serializers.FileField(validators=[FileExtensionValidator(['csv'])])

class DataSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Dataset
        fields = ('id','name','date')