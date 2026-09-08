
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    CATEGORY_CHOICES = [
        ("cultural", "Cultural / Ethnic"),
        ("neighborhood", "Neighborhood"),
        ("religious", "Religious / Spiritual"),
        ("professional", "Professional"),
        ("education", "Education / Students"),
        ("family", "Parents / Families"),
        ("sports", "Sports"),
        ("health", "Health / Wellness"),
        ("meditation", "Meditation"),
        ("technology", "Technology"),
        ("arts", "Arts / Music"),
        ("volunteer", "Volunteer / Nonprofit"),
        ("business", "Business"),
        ("hobby", "Hobbies / Social"),
        ("lgbtq", "LGBTQ+"),
        ("youth_senior", "Seniors / Youth"),
        ("other", "Other"),
    ]

    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("members", "Members Only"),
        ("private", "Private"),
    ]

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="other",
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default="public",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_communities",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Communities"

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("member", "Member"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("banned", "Banned"),
    ]

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_memberships",
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="member",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active",
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["community", "user"],
                name="unique_community_membership",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.community.name}"
