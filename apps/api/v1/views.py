from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers

class DatasetAPIView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self, reques, format=None):
        an_apiview=['Hola']
        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message= f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class RowAPIView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self, reques, format=None):
        an_apiview=['Hola']
        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message= f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )