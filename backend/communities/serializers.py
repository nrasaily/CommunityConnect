from rest_framework import serializers
from .models import Community


class CommunitySerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(
        source="owner.username",
        read_only=True
    )

    class Meta:
        model = Community

        fields = [
            "id",
            "name",
            "description",
            "category",
            "location",
            "privacy",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        ]
