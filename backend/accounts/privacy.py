def can_view_contact(profile, viewer, visibility):
    """
    Decide whether a viewer can see a user's contact information.

    visibility can be:
    - private
    - members
    - public
    """

    if visibility == "public":
        return True

    if not viewer.is_authenticated:
        return False

    if viewer == profile.user:
        return True

    if visibility == "private":
        return False

    if visibility == "members":
        from communities.models import Membership

        profile_user_communities = Membership.objects.filter(
            user=profile.user,
            status="active",
        ).values("community_id")

        return Membership.objects.filter(
            user=viewer,
            status="active",
            community_id__in=profile_user_communities,
        ).exists()

    return False


def can_view_phone(profile, viewer):
    return can_view_contact(
        profile,
        viewer,
        profile.phone_visibility
    )


def can_view_email(profile, viewer):
    return can_view_contact(
        profile,
        viewer,
        profile.email_visibility
    )
