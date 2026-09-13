from django.db import transaction
from django.db.models import Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Community, Membership
from .serializers import CommunitySerializer


class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all().order_by("-created_at")
    serializer_class = CommunitySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    filterset_fields = [
        "category",
        "location",
        "privacy",
    ]

    search_fields = [
          "name",
          "description",
          "location",
          "category",
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
    
