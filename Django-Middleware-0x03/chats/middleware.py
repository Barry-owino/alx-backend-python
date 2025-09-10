# chats/middleware.py

import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")  # log file in project root
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Get user info
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        
        # Log request info
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        # Continue processing request
        response = self.get_response(request)
        return response

