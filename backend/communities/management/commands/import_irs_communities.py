import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from communities.models import Community, Membership


class Command(BaseCommand):
    help = "Import real organizations from an IRS EO BMF CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the IRS CSV file"
        )

        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of organizations to import"
        )

    def map_category(self, ntee_code):
        if not ntee_code:
            return "other"

        letter = ntee_code[0].upper()

        category_map = {
            "A": "arts",
            "B": "education",
            "E": "health",
            "F": "health",
            "G": "health",
            "H": "health",
            "J": "professional",
            "N": "sports",
            "O": "youth_senior",
            "S": "neighborhood",
            "U": "technology",
            "X": "religious",
        }

        return category_map.get(letter, "other")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        limit = options["limit"]

        seed_user, created = User.objects.get_or_create(
            username="directory_seed"
        )

        if created:
            seed_user.set_unusable_password()
            seed_user.save()

        created_count = 0
        skipped_count = 0

        with open(csv_file, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if limit and created_count >= limit:
                    break

                name = row.get("NAME", "").strip()
                city = row.get("CITY", "").strip()
                state = row.get("STATE", "").strip()
                ntee_code = row.get("NTEE_CD", "").strip()

                if not name:
                    skipped_count += 1
                    continue

                location = ", ".join(
                    part for part in [city, state] if part
                )

                category = self.map_category(ntee_code)

                community, was_created = Community.objects.get_or_create(
                    name=name,
                    location=location,
                    defaults={
                        "description": "Organization listed in the IRS Exempt Organizations Business Master File.",
                        "category": category,
                        "privacy": "public",
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

                if was_created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created: {community.name}"
                        )
                    )
                else:
                    skipped_count += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {created_count}"
            )
        )
        self.stdout.write(
            f"Skipped/already existed: {skipped_count}"
        )