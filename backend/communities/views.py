from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response

from .models import Community, Membership
from .serializers import CommunitySerializer



class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all().order_by("-created_at")
    serializer_class = CommunitySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "location",
        "privacy",
    ]
    ordering_fields = [
        "name",
        "location",
        "category",
        "created_at",
    ]
    search_fields = [
          "name",
          "description",
          "location",
          "category",
    ]
    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        queryset = Community.objects.all().order_by("-created_at")
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(privacy="public")
        
        return queryset.filter(
            Q(privacy="public")
            | Q(owner=user)
            | Q(
                memberships__user=user,
                memberships__status="active"
            )
        ).distinct()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
    
    @transaction.atomic
    def perform_create(self, serializer):
        community = serializer.save(owner=self.request.user)

        Membership.objects.create(
          community=community,
          user=self.request.user,
          role="owner",
          status="active",
        )

class CommunityDetailView(generics.RetrieveAPIView):
    serializer_class = CommunitySerializer

    def get_queryset(self):
        queryset = Community.objects.all()
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(privacy="public")

        return queryset.filter(
            Q(privacy="public")
            | Q(owner=user)
            | Q(
                memberships__user=user,
                memberships__status="active"
            )
        ).distinct()
    
# PSEUDOCODE:

# Create a JoinCommunityView

# Require the user to be logged in

# When the user sends a POST request:
#     Get the community ID from the URL

#     Find that community in the database

#     If the community does not exist:
#         Return 404 Not Found

#     Check whether this user already has a Membership
#     for this community

#     If membership already exists:
#         Return a message such as:
#         "You already joined or already requested to join"

#     If the community is public:
#         Create Membership
#         role = "member"
#         status = "active"

#         Return:
#         "Successfully joined community"

#     If the community is private:
#         Create Membership
#         role = "member"
#         status = "pending"

#         Return:
#         "Join request sent for approval"

#     If the community uses members-only privacy:
#         Decide whether it should behave like public
#         or require approval


class JoinCommunityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(current_view, request, pk):
        community = get_object_or_404(
            Community,
            pk=pk
        )

        existing_membership = Membership.objects.filter(
            community=community,
            user=request.user
        ).first()

        if existing_membership:
            return Response(
                {
                    "detail": "You already joined or requested to join this community.",
                    "status": existing_membership.status
                },
                status=status.HTTP_200_OK
            )

        if community.privacy == "public":
            membership_status = "active"
            message = "You are community member now."
        else:
            membership_status = "pending"
            message = "Your membership request is pending. Join request has been sent."

        Membership.objects.create(
            community=community,
            user=request.user,
            role="member",
            status=membership_status
        )

        return Response(
            {
                "detail": message,
                "community_id": community.id,
                "community_name": community.name,
                "membership_status": membership_status
            },
            status=status.HTTP_201_CREATED
        )
    
        
class ApproveMembershipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, membership_id):
        community = get_object_or_404(
            Community,
            pk=pk
        )

        if request.user != community.owner:
            return Response(
                {
                    "detail": "Only the community owner can approve join requests."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        membership = get_object_or_404(
            Membership,
            id=membership_id,
            community=community,
            status="pending"
        )

        membership.status = "active"
        membership.save()

        return Response(
            {
                "detail": "Membership request approved.",
                "membership_id": membership.id,
                "username": membership.user.username,
                "membership_status": membership.status
            },
            status=status.HTTP_200_OK
        )
    
class RejectMembershipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, membership_id):
        community = get_object_or_404(
            Community,
            pk=pk
        )

        if request.user != community.owner:
            return Response(
                {
                    "detail": "Only the community owner can reject join requests."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        membership = get_object_or_404(
            Membership,
            id=membership_id,
            community=community,
            status="pending"
        )

        username = membership.user.username
        membership.delete()

        return Response(
            {
                "detail": "Membership request rejected.",
                "username": username
            },
            status=status.HTTP_200_OK
        )