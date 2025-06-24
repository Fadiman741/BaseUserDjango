import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from users.models import User

from django.contrib.auth import authenticate, login, logout
from .serializers import (
    UserSerializer
)

from rest_framework.authentication import TokenAuthentication

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer

# ======================AUTHENTICATION========================================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])
        user.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({'error': 'User not authenticated'})

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_current_user(request):
    serializer = UserSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "Email": user.email,
                "Occupation": user.occupation,
            }
        )
    return Response({"error": "Invalid credentials"}, status=401)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"success": "Logged out successfully"})

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterLoginSerializer

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/accounts/google/login/callback/"
    client_class = OAuth2Client

@api_view(['POST'])
@permission_classes([AllowAny])
def social_auth(request):
    provider = request.data.get('provider')
    access_token = request.data.get('access_token')
    token_secret = request.data.get('token_secret')  # For Twitter
    
    if not provider or not access_token:
        return Response(
            {'error': 'Provider and access token are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if provider == 'google':
            from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
            adapter = GoogleOAuth2Adapter(request)
        elif provider == 'facebook':
            from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
            adapter = FacebookOAuth2Adapter(request)
        elif provider == 'twitter':
            from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
            adapter = TwitterOAuthAdapter(request)
            # Twitter requires token_secret
            if not token_secret:
                return Response(
                    {'error': 'Token secret is required for Twitter'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'Invalid provider'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = adapter.complete_login(request, None, access_token, token_secret)
        user = token.account.user
        
        # Generate or get existing token
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )