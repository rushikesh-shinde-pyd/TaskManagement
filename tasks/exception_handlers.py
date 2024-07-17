from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled, AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        return Response(
            {'detail': 'Rate limit exceeded. Please try again later'},
            status=429
        )

    if isinstance(exc, AuthenticationFailed):
        response_data = {
            'error': 'Authentication failed.',
            'detail': 'Token is invalid or expired'
        }
        response = Response(response_data, status=401)


    return response