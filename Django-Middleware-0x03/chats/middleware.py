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

import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Existing middleware
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


# New middleware for time restriction
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict only the chat/messaging path
        if request.path.startswith("/chat/"):
            current_hour = datetime.now().hour
            # Deny access outside 6 PM (18) to 9 PM (21)
            if current_hour < 18 or current_hour >= 21:
                return HttpResponseForbidden("Chat is only available from 6 PM to 9 PM.")

        response = self.get_response(request)
        return response

