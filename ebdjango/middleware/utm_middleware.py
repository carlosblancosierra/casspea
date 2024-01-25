# utm_middleware.py

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class UTMMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.include_parameters = getattr(settings, 'UTMMIDDLEWARE_INCLUDE_PARAMETERS', [])

    def __call__(self, request):
        try:
            # Access UTM codes from the request's GET parameters
            for param in self.include_parameters:
                value = request.GET.get(param)
                if value is not None:
                    request.session[param] = value
                    request.session.set_expiry(getattr(settings, 'UTMMIDDLEWARE_SESSION_EXPIRY', 24 * 60 * 60))  # Default to 24 hours
        except Exception as e:
            logger.error(f"Error in UTMMiddleware: {e}")

        response = self.get_response(request)
        return response
