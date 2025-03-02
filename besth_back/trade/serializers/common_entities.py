from rest_framework import serializers
from django.core.validators import MinValueValidator
from decimal import Decimal

from trade.models import FuelType, OilBase


class OilBaseSerializer(serializers.ModelSerializer):
    ksss_code = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    class Meta:
        model = OilBase
        fields = ['id', 'ksss_code', 'name', 'region', 'address']


class FuelTypeSerializer(serializers.ModelSerializer):
    ksss_code = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = FuelType
        fields = ['id', 'ksss_code', 'name', 'description']
