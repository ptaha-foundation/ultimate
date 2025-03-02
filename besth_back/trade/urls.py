from rest_framework import routers
from django.urls import include, path
from trade.views import LotViewSet, FuelTypeViewSet, OilBaseViewSet, OrderViewSet, CSVUploadView


router = routers.DefaultRouter()
router.register(r'lots', LotViewSet, basename='lots')
router.register(r'fuel-types', FuelTypeViewSet, basename='fuel-types')
router.register(r'oil-bases', OilBaseViewSet, basename='oil-bases')
router.register(r'orders', OrderViewSet, basename='orders')
# router.register(r'upload-csv', CSVUploadView, basename='upload-csv')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv')
]
