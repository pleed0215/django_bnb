import random

from django.core.management.base import BaseCommand

from django_seed import Seed

from users.models import User
from rooms.models import Room
from reviews.models import Review


class Command(BaseCommand):
    help = "This command will seed reviews for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=50,
            type=int,
            help="How many dummy reviews do you want make?",
        )

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        number = options.get("number", 1)
        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(
                f"{number} review{number>1 and 's' or ''} are succefully made."
            )
        )

