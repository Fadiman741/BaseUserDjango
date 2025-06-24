from django.urls import path

from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import (
    signup,
    logout_view,
    login_view, 
    get_current_user,
    update_current_user,
    social_auth,
)

schema_view = get_schema_view(
    openapi.Info(
        title="BASE USER DJANGO",
        default_version='v1',
        description=(
            "This defines the core authentication and user management endpoints "
            "for the Base User system in a Django REST Framework project.\n\n"
            "Available endpoints include:\n"
            "- User sign-up, login, and logout\n"
            "- Fetching and updating the currently authenticated user\n"
            "- Social authentication using Google OAuth\n"
            "- Interactive API documentation powered by Swagger and ReDoc (via drf-yasg)"
        ),
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@yourapi.local"),
    #   license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
    
from .views import GoogleLogin,FacebookLogin, TwitterLogin

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # path("create_comment/", create_comment, name="create_comment"),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('update_current_user   /', update_current_user,name='update_current_user'),

    # Social auth endpoints
    path('social-auth/', social_auth, name='social_auth'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('social-auth/', social_auth, name='social_auth'),

    # Swagger/OpenAPI URLs
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# =======================================================================================
