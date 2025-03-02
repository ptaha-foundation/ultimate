from django.contrib import admin

from trade.models import Lot, Order, OilBase, FuelType

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    search_fields = ('id', 'oil_base', 'fuel_type', 'status')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('id', 'client', 'lot', 'delivery_type', 'status')


@admin.register(OilBase)
class OilBaseAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'ksss_code')


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'ksss_code')
