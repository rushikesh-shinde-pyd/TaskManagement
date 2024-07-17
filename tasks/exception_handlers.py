# Third-party imports
from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled, AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    This function handles exceptions raised during request processing and customizes the error response
    based on the type of exception encountered.
    """
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