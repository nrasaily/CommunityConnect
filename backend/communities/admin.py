
# Register your models here.
from django.contrib import admin
from .models import Community, Membership


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "location",
        "privacy",
        "owner",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "location",
        "owner__username",
    )

    list_filter = (
        "category",
        "privacy",
        "created_at",
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "community",
        "role",
        "status",
        "joined_at",
    )

    search_fields = (
        "user__username",
        "community__name",
    )

    list_filter = (
        "role",
        "status",
        "joined_at",
    )
