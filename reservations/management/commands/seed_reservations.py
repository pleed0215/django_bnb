import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from users.models import User
from rooms.models import Room
from reservations.models import Reservation


class Command(BaseCommand):
    help = "This command will seed reservations for development."
    checkin = datetime.now()
    checkout = datetime.now()

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=50,
            type=int,
            help="How many dummy reservations do you want make?",
        )

    def random_checkin(self):
        self.checkin = datetime(
            random.randint(2010, 2025), random.randint(1, 12), 1
        ) + timedelta(days=random.randint(0, 27))
        return self.checkin

    def random_checkout(self):
        self.checkout = self.checkin + timedelta(days=random.randint(0, 30))
        return self.checkout

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        number = options.get("number", 1)
        users = User.objects.all()
        rooms = Room.objects.all()

        statuses = ["peding", "confirmed", "canceled"]

        for i in range(0, number):

            seeder.add_entity(
                Reservation,
                1,
                {
                    "status": lambda x: random.choice(statuses),
                    "guest": lambda x: random.choice(users),
                    "room": lambda x: random.choice(rooms),
                    "checkin_date": lambda x: self.random_checkin(),
                    "checkout_date": lambda x: self.random_checkout(),
                },
            )

        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(
                f"{number} reservation{number>1 and 's' or ''} are succefully made."
            )
        )

