import pandas as pd
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from trade.serializers import FileUploadSerializer
from trade.services import CSVLotsProcessingService


logger = logging.getLogger('common')


class CSVUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.info("Processing CSV upload request...")
        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_obj = serializer.validated_data['file']
        if not file_obj.name.endswith('.csv'):
            return Response(
                {"error": "File must be a CSV file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(file_obj)
            processor = CSVLotsProcessingService(df)
            result = processor.process()

            if not result["success"]:
                return Response(
                    {"error": result["error"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            return Response(
                {"error": f"Failed to process CSV file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
