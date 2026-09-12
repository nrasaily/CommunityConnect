from rest_framework import serializers

from .models import Profile
from communities.models import Membership


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Profile

        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "bio",
            "location",
            "phone_visibility",
            "email_visibility",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "email",
            "created_at",
            "updated_at",
        ]

    def users_share_community(self, profile_user, viewer):
        viewer_communities = Membership.objects.filter(
            user=viewer,
            status="active",
        ).values_list("community_id", flat=True)

        return Membership.objects.filter(
            user=profile_user,
            status="active",
            community_id__in=viewer_communities,
        ).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        viewer = request.user if request else None

        # The profile owner can always see their own information.
        if viewer and viewer.is_authenticated and viewer == instance.user:
            return data

        shares_community = False

        if viewer and viewer.is_authenticated:
            shares_community = self.users_share_community(
                instance.user,
                viewer,
            )

        if instance.phone_visibility == "private":
            data.pop("phone_number", None)

        elif (
            instance.phone_visibility == "members"
            and not shares_community
        ):
            data.pop("phone_number", None)

        if instance.email_visibility == "private":
            data.pop("email", None)

        elif (
            instance.email_visibility == "members"
            and not shares_community
        ):
            data.pop("email", None)

        return data