from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import json


# Create your views here.
@api_view(["POST"])
def register(request,*args,**kwargs):
    data = request.data
    if data is None:
        return Response({"error":"provide data for registering the user"})
    serializer = UserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
def login(request,*args, **kwargs):
    data = request.data
    if not data:
        return Response({"error": "provide credentials for login"}, status=status.HTTP_400_BAD_REQUEST)
    
    email = data.get('email')
    password = data.get('password')
    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)
        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value=tokens['access'], 
            httponly=True, 
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
            value=tokens['refresh'], 
            httponly=True, 
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        )
        return response
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def refresh_token(request,*args, **kwargs):
    refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

    if refresh_token is None:
        return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token

        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value=str(new_access_token), 
            httponly=True, 
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )
        return response

    except Exception as e:
        return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request, *args, **kwargs):
    user_id = request.user.id
    email = request.user.email
    data = json.dumps({"id":user_id,"email":email})
    return Response({"message": "You have access to this protected route","data":data}, status=status.HTTP_200_OK)

@api_view(["POST"])
def logout(request):
    response = Response({"message": "Successfully signed out"}, status=status.HTTP_200_OK)
    
    # Clear the access token cookie
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])

    # Clear the refresh token cookie
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
    
    return response