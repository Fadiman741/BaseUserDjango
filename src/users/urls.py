from django.urls import path
from .views import (
    signup,
    logout_view,
    login_view, 
    get_current_user,
    update_current_user,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # path("create_comment/", create_comment, name="create_comment"),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('update_current_user   /', update_current_user,name='update_current_user'),

]
# =======================================================================================
