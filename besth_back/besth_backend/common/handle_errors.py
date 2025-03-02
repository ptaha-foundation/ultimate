from rest_framework.response import Response
from rest_framework import status


# TODO переписать обработку валидации полей во всех моделях
def handle_validation_errors(errors):
    field_name = list(errors.keys())[0]
    error = str(errors[field_name][0])
    return Response({ 'message': f'{ field_name } - { error }' }, status=status.HTTP_400_BAD_REQUEST)
