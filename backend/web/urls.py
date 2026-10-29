from django.urls import path

from .views import community_list_view, home_view


urlpatterns = [
    path("", home_view, name="home"),
    path(
        "communities/",
        community_list_view,
        name="community-list",
    ),
]