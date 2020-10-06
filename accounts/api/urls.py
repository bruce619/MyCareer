from django.urls import path
from rest_framework.routers import format_suffix_patterns
from .views import *


urlpatterns = [
    path('users/register/', UserCreateAPIView.as_view(), name="register"),
    path('users/auth/', obtain_auth_token, name='auth'),
    path('all-users/', get_all_user_api_view, name="all-users"),
    path('profile/', get_update_profile_api_view, name="profile")

]

urlpatterns = format_suffix_patterns(urlpatterns)
