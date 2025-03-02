from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from trade.models import Lot
from trade.serializers import LotSerializer, LotRetrieveSerializer, LotListSerializer
from trade.filters import LotFilter

from besth_backend.common import handle_validation_errors


class LotViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LotFilter
    search_fields = ['oil_base__name', 'oil_base__address', 'fuel_type__name']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return LotRetrieveSerializer
        return LotSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            lot = serializer.save()
            lot.client = self.request.user
            lot.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return handle_validation_errors(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return handle_validation_errors(serializer.errors)
