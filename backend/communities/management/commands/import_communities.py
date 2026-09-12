import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from communities.models import Community, Membership


class Command(BaseCommand):
    help = "Import communities from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        seed_user, created = User.objects.get_or_create(
            username="directory_seed"
        )

        if created:
            seed_user.set_unusable_password()
            seed_user.save()

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                description = row.get("description", "").strip()
                category = row.get("category", "other").strip()
                location = row.get("location", "").strip()
                privacy = row.get("privacy", "public").strip()

                community, community_created = Community.objects.get_or_create(
                    name=name,
                    location=location,
                    defaults={
                        "description": description,
                        "category": category,
                        "privacy": privacy,
                        "owner": seed_user,
                    }
                )

                Membership.objects.get_or_create(
                    community=community,
                    user=seed_user,
                    defaults={
                        "role": "owner",
                        "status": "active",
                    }
                )

                if community_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created: {community.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"Already exists: {community.name}"
                    )