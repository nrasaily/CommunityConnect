from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "location",
        "phone_visibility",
        "email_visibility",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
        "location",
    )

    list_filter = (
        "phone_visibility",
        "email_visibility",
        "created_at",
    )
# Register your models here.
