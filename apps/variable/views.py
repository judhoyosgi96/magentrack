from django.shortcuts import render 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from pymongo import MongoClient
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

def index (request):    
    return render(request, 'index.html') 




class LogAPIView(APIView):
    """This is the view for log api"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        client = MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
        db = client[settings.MONGO_DB_NAME]
        collection = db[settings.MONGO_DB_COLLECTION_NAME]
        result=list(collection.find({}, {'ip':1,'time':1,'user':1, '_id':0}))
        return Response(result)

