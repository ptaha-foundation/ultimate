from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from trade.models import OilBase, FuelType
from trade.serializers import FuelTypeSerializer, OilBaseSerializer

from besth_backend.common import handle_validation_errors


class FuelTypeViewSet(viewsets.ModelViewSet):
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return handle_validation_errors(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializer_class(instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return handle_validation_errors(serializer.errors)


class OilBaseViewSet(viewsets.ModelViewSet):
    queryset = OilBase.objects.all()
    serializer_class = OilBaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
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
