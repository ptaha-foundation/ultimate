from rest_framework import serializers
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal

from trade.models import Order, Lot, OilBase, FuelType


    # ['lot', 'oil_base', 'fuel_type', 'volume', 'delivery_type', 'client', 'price', 'delivery_address']


class OrderSerializer(serializers.ModelSerializer):
    lot = serializers.PrimaryKeyRelatedField(queryset=Lot.objects.all(), required=False)
    oil_base = serializers.PrimaryKeyRelatedField(queryset=OilBase.objects.all(), required=False)
    fuel_type = serializers.PrimaryKeyRelatedField(queryset=FuelType.objects.all(), required=False)
    volume = serializers.DecimalField(
                                max_digits=12,
                                decimal_places=6,
                                validators=[MinValueValidator(Decimal('0.000000'))],
                                required=False)
    delivery_type = serializers.CharField(required=False)
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    price = serializers.DecimalField(
                                max_digits=12,
                                decimal_places=6,
                                validators=[MinValueValidator(Decimal('0.01'))],
                                required=False)
    delivery_address = serializers.CharField(required=False) 

    class Meta:
        model = Order
        fields = ['id', 'lot', 'oil_base', 'fuel_type', 'volume', 'delivery_type', 'client', 'price', 'delivery_address']
