from django.urls import path
from .views import CommunityListCreateView


urlpatterns = [
    path("", CommunityListCreateView.as_view(), name="community-list-create"),
]
