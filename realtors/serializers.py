from rest_framework import serializers
from .models import *
class RealtorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Realtor
        fields="__all__"

