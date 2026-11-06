from django.urls import path

from .views import community_list_view, home_view

from . import views

urlpatterns = [
    path("", home_view, name="home"),
    path(
        "communities/",
        community_list_view,
        name="community-list",
    ),
    path(
        "communities/create/",
        views.community_create,
        name="community_create",
),
]
