import time

import logging

logger = logging.getLogger(__name__)

class RequestElapsedTimeMiddleware:
    """
    Simple middleware that logs the elapsed time for each request processing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_path_info = request.META.get('PATH_INFO')
        start_time = time.time()
        response = self.get_response(request)
        logger.info(f'Elapsed time {time.time() - start_time:.2f} - {request_path_info}')
        return response