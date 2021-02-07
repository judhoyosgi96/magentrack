from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=95)
    file=serializers.CharField(max_length=100)