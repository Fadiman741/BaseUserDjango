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

