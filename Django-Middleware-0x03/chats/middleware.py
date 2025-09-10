# chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict

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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track messages per IP: {ip: [timestamps]}
        self.ip_message_times = defaultdict(list)
        self.limit = 5          # max messages
        self.time_window = 60   # time window in seconds (1 minute)

    def __call__(self, request):
        # Only count POST requests (sending messages)
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = self.get_client_ip(request)
            now = time.time()
            # Keep only timestamps within the last minute
            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if now - t < self.time_window]

            if len(self.ip_message_times[ip]) >= self.limit:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            # Record this message timestamp
            self.ip_message_times[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Standard method to get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict access to certain paths, e.g., /admin-actions/
        if request.path.startswith("/admin-actions/"):
            user = request.user
            # Check if user is authenticated and has required role
            if not user.is_authenticated or not getattr(user, 'role', None) in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        # Continue processing request
        response = self.get_response(request)
        return response

