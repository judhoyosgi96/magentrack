
from django.urls import path
from .views import DatasetAPIView,RowAPIView

urlpatterns = [
    path('datasets/', DatasetAPIView.as_view()),
    path('rows/', RowAPIView.as_view()),
]
