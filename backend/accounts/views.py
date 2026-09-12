from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken




from .models import Profile
from .serializers import ProfileSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#------------------------------------------------------------------------------------------------

# Create your views here.

# PSEUDOCODE:
# Create an API endpoint for the currently logged-in user's profile
# Require the user to be logged in
# When the user requests their profile:
#     Get the Profile that belongs to the logged-in user
#     If the profile does not exist, return 404
#     Check that the user has permission to access the profile
#     Return the user's profile
# Allow the user to retrieve or update their profile

# User sends request
#       ↓
# Is user authenticated?
#       ↓
# Find profile belonging to that user
#       ↓
# Check permission
#       ↓
# Return profile

class MyProfileView(generics.RetrieveUpdateAPIView):

    # User sends request
    # Django sends the request to MyProfileView
    serializer_class = ProfileSerializer

    # Is user authenticated?
    permission_classes = [IsAuthenticated]
    def get_object(self):

        # Find profile belonging to that user
        profile = get_object_or_404(
            Profile,
            user=self.request.user
        )

        # Check permission
        self.check_object_permissions(
            self.request,
            profile
        )

        # Return profile
        return profile
    
    #------------------------------------------------------------------------------------------------

# PSEUDOCODE:
# Create a logout API endpoint
# When a POST request is received:
#     Get the refresh token from the request
#     Try to convert it into a RefreshToken object
#     Blacklist the refresh token
#     Return "Successfully logged out" with HTTP 205
# If an error occurs:
#     Return "Invalid refresh token" with HTTP 400

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)
            token.blacklist()
            # It takes the user's refresh token and puts it on the blacklist.
            #  After that, that refresh token cannot be used to generate another access token.

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# PSEDOCODE:
# Create a logout endpoint
#Recieve a Post request from user 
#Get a refresh token from the request body
#try to turn that string into a Refresh Token object
#Add the refresh token to the blacklist
#Return a successful logout response
#if the refresh token is missing, expired, invalid, or another error happense return a invalid refresh token" response

#------------------------------------------------------------------------------------------------
# PSEUDOCODE:
# Create an API endpoint for viewing another user's profile
# Require the viewer to be logged in
# Get the profile ID from the URL
# Search the Profile table for that ID
#
# If the profile does not exist:
# Return 404 Not Found
#
# Check whether the viewer has permission to access the profile
# Send the profile to ProfileSerializer
# Return the serialized profile data

# Example:
# GET /api/accounts/profiles/2/
#               ↓
# Django gets pk = 2
#               ↓
# Find Profile with id = 2
#               ↓
# Check permissions
#               ↓
# Serialize profile
#               ↓
# Return profile JSON

class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): 
        profile = get_object_or_404(
            Profile,
            id=self.kwargs["pk"]
        )
        self.check_object_permissions(
            self.request,
            profile
        )

        return profile
#------------------------------------------------------------------------------------------------
