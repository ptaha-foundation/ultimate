from rest_framework import serializers
from trade.models import Lot, OilBase, FuelType
from decimal import Decimal
from django.core.validators import MinValueValidator


class LotSerializer(serializers.ModelSerializer):
    oil_base = serializers.PrimaryKeyRelatedField(queryset=OilBase.objects.all(), required=False)
    fuel_type = serializers.PrimaryKeyRelatedField(queryset=FuelType.objects.all(), required=False)
    expiration_date = serializers.DateField(required=False)
    initial_volume = serializers.DecimalField(
                                max_digits=12,
                                decimal_places=6,
                                required=False)
    available_volume = serializers.DecimalField(
                                max_digits=12,
                                decimal_places=6,
                                required=False)
    status = serializers.CharField(required=False)
    price_per_ton = serializers.DecimalField(
                                max_digits=10,
                                decimal_places=2,
                                required=False)    

    class Meta:
        model = Lot
        fields = ['expiration_date', 'oil_base', 'fuel_type', 'initial_volume', 'available_volume', 'status', 'price_per_ton']

    def validate_initial_volume(self, value):
        if value < Decimal('0.000000'):
            raise serializers.ValidationError("Стартовый объём не может быть меньше 0.")
        return value

    def validate_price_per_ton(self, value):
        if value < Decimal('0.01'):
            raise serializers.ValidationError("Цена за тонну должна быть больше 0.01.")
        return value


class LotRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ['id', 'expiration_date', 'oil_base', 'fuel_type', 'initial_volume',
                  'status', 'total_price', 'price_per_ton', 'available_volume']


class LotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ['id', 'expiration_date', 'oil_base', 'fuel_type', 'available_volume', 'status']
