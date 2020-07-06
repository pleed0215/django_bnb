from django.core.management.base import BaseCommand
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command will seed facilities for development."

    """
    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            default=50,
            type=int,
            help="How many dummy rooms do you want make?",
        )
    """

    def handle(self, *args, **options):
        facilities = [
            "Spa",
            "Semi open & outdoor restaurant",
            "Poolside bar",
            "Car parking",
            "Swimming pool/ Jacuzzi",
            "Public computer",
            "Disable rooms & Interconnecting rooms",
            "24 Hour security",
            "Outside catering service",
            "100 Seating capacity restaurant",
            "150 Capacity outdoor terrace",
            "45 Seating conference room",
            "35 Seating private air-conditioning dining room",
            "Water purification system",
            "Sunset boat trip",
            "Gift shop",
        ]

        for f in facilities:
            rooms_models.Facility.objects.create(name=f)
        self.stdout.write(
            self.style.SUCCESS(f"{len(facilities)} facilities succefully made.")
        )

