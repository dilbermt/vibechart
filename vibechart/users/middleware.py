from django.conf import settings
from django.urls import resolve
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken


class JWTAuthenticationFromCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url_name = resolve(request.path_info).url_name

        if current_url_name != "refresh-token" and current_url_name != "login":
            access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
            if access_token:
                # Set the access token in the Authorization header as "Bearer <token>"
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.get_response(request)


        return response
