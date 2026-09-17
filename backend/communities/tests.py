from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Community


class CommunityFilterTests(APITestCase):
    def setUp(self):
        self.url = "/api/communities/"

        self.owner = User.objects.create_user(
            username="test_owner",
            password="TestPassword123!",
        )

        Community.objects.create(
            name="Rochester Health Group",
            description="A public healthcare organization",
            category="health",
            location="ROCHESTER, NY",
            privacy="public",
            owner=self.owner,
        )

        Community.objects.create(
            name="Private Rochester Group",
            description="This community must remain private",
            category="health",
            location="ROCHESTER, NY",
            privacy="private",
            owner=self.owner,
        )

    def test_filter_by_category(self):
        response = self.client.get(
            self.url,
            {"category": "health"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Rochester Health Group",
        )

    def test_private_community_is_hidden(self):
        response = self.client.get(
            self.url,
            {"privacy": "private"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_filtered_results_are_paginated(self):
        for number in range(21):
            Community.objects.create(
                name=f"Arts Community {number}",
                description="A public arts community",
                category="arts",
                location="NEW YORK, NY",
                privacy="public",
                owner=self.owner,
            )

        response = self.client.get(
            self.url,
            {"category": "arts"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 21)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])