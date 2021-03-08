from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import *

class RealtorsView(viewsets.ModelViewSet):
    queryset = Realtor.objects.all()
    serializer_class = RealtorsSerializer

