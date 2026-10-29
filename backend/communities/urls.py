from django.urls import path
from .views import ( 
  CommunityListCreateView,
  CommunityDetailView,
  JoinCommunityView,
  ApproveMembershipView,
  RejectMembershipView,
)


urlpatterns = [
    path("", CommunityListCreateView.as_view(), name="community-list-create"),
    path("<int:pk>/", CommunityDetailView.as_view(), name="community-detail"),
    path("<int:pk>/join/", JoinCommunityView.as_view(), name="community-join-view"),
    path( "<int:pk>/memberships/<int:membership_id>/approve/", ApproveMembershipView.as_view(),
    name="membership-approve"),
    path(
    "<int:pk>/memberships/<int:membership_id>/reject/",
    RejectMembershipView.as_view(),
    name="membership-reject",
),
]
