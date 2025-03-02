from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

import logging


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This view is protected"})



logger = logging.getLogger('common')

# Example usage in views
def my_view(request):
    logger.info('View executed successfully.')
    return HttpResponse('abc')
