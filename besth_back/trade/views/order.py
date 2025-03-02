from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from trade.models import Order
from trade.serializers import OrderSerializer

from besth_backend.common import handle_validation_errors


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            order = Order(**serializer.validated_data)
            order.client = self.request.user
            order.price = order.lot.price_per_ton
            order.fuel_type = order.lot.fuel_type
            order.oil_base = order.lot.oil_base
            if order.volume > order.lot.available_volume:
                return Response({'message': 'Недостаточно топлива для покупки'}, status=status.HTTP_400_BAD_REQUEST)
                
            order.save()
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
