from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import serializers
from django.utils import timezone
from django.conf import settings

from django.http import HttpResponse
from django.forms.models import model_to_dict

from apps.dataset.models import Dataset
from apps.row.models import Row
from apps.variable.models import Variable

from rest_framework.permissions import IsAuthenticated

from pymongo import MongoClient

import csv

from django.contrib.gis.geos import Point


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log(request):    
    ip = get_client_ip(request)
    time = timezone.now()
    user = request.user.get_username()
    if user == '':
        user = 'None'
    client = MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
    db = client[settings.MONGO_DB_NAME]
    collection = db[settings.MONGO_DB_COLLECTION_NAME]
    newlog = { "ip": ip, "time": time, "user": user }
    collection.insert_one(newlog)

class DatasetAPIView(APIView):
    """This is the view for dataset api"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DatasetSerializer

    def get(self, request, format=None):
        log(request)    

        data = Dataset.objects.all()
        data_json = [model_to_dict(my_record) for my_record in data]

        items_per_page = Variable.objects.get(name='items_per_page').value
        
        paginator = Paginator(data,items_per_page)
        page_num = self.request.query_params.get('page', None)
        if page_num is None:
            # If page is not provided show all
            return Response(data_json)
        try:
            data = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            data = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            data = paginator.page(paginator.num_pages)
        serializer = serializers.DataSerializer(data, many=True)

        return Response(serializer.data)

    
    def post(self, request):
        log(request)

        serializer = self.serializer_class(data=request.data)        
        if serializer.is_valid():
            now = timezone.now()
            name=serializer.validated_data.get('name')
            d = Dataset.objects.create(name=name,date=now) # Create new dataset object

            file = request.FILES['file'] 
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Row.objects.create(dataset_id=d,
                point=Point(float(row['longitude']),float(row['latitude'])),
                client_id=row['client_id'],
                client_name=row['client_name']) # Create new row object

            message= f'File {name} was seccesfully uploaded'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class RowAPIView(APIView):
    """This is the view for row api"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        log(request)
        
        dataset_id = self.request.query_params.get('dataset_id', None)
        if dataset_id is None or not dataset_id.isnumeric():
            return Response(
                {"message":"Must provide a valid dataset_id filter : /api/v1/rows?dataset_id=<dataset_id>"},
                status=status.HTTP_400_BAD_REQUEST
            )       

        data = Row.objects.filter(dataset_id=dataset_id)

        name = self.request.query_params.get('name', None)
        if name is not None:
            data = data.filter(client_name=name)

        point_xy = self.request.query_params.get('point', None)

        if point_xy is not None:
            try: 
                point_xy=point_xy[point_xy.find("(")+1:point_xy.find(")")].split(" ")
                print(point_xy)
                point=Point(float(point_xy[0]),float(point_xy[1]))
                data = data.filter(point__coveredby=point)
            except:
                return Response(
                {"message":"Must provide a valid point filter : /api/v1/rows?dataset_id=<dataset_id>&point=(<lon> <lat>)"},
                status=status.HTTP_400_BAD_REQUEST
                )  

        data_json = [{'id' : my_record.id,
                    'dataset_id' : str(my_record.dataset_id.id),
                    'point' : str(my_record.point),
                    'client_id' : my_record.client_id, 
                    'client_name' : my_record.client_name} for my_record in data]
        return Response(data_json)
