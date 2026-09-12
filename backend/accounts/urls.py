from django.urls import path
from .views import MyProfileView
from .views import LogoutView
from .views import PublicProfileView
urlpatterns = [
    path("profile/", MyProfileView.as_view(), name="my-profile"), 
    #URL → View → Authentication → Profile → Serializer → Response
    
    path("logout/", LogoutView.as_view(), name="logout"),

    path("profiles/<int:pk>/", PublicProfileView.as_view(), name="public-profile")
]


# User sends POST request to /logout/
#       ↓
# Django finds this URL
#       ↓
# Send request to LogoutView
#       ↓
# LogoutView blacklists the refresh token
#or
# POST /logout/
#       ↓
# path("logout/", LogoutView.as_view(), name="logout")
#       ↓
# LogoutView
#       ↓
# post()
#       ↓
# Get refresh token
#       ↓
# Blacklist refresh token
#       ↓
# Return "Successfully logged out"