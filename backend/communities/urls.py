from django.urls import path
from .views import CommunityListCreateView, CommunityDetailView


urlpatterns = [
    path("", CommunityListCreateView.as_view(), name="community-list-create"),
    path("<int:pk>/", CommunityDetailView.as_view(), name="community-detail"),
]
