import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from users.models import User
from rooms.models import Room
from lists.models import List


class Command(BaseCommand):
    help = "This command will seed lists for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=50,
            type=int,
            help="How many dummy lists do you want make?",
        )

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        number = options.get("number", 1)
        users = User.objects.all()
        rooms = Room.objects.all()

        room_count = Room.objects.count()
        max_count = room_count > 20 and 20 or room_count
        min_count = room_count < 5 and room_count or 5

        seeder.add_entity(
            List, number, {"user": lambda x: random.choice(users),},
        )
        created_pk = seeder.execute()
        cleaned_pk = flatten(list(created_pk.values()))

        for pk in cleaned_pk:
            my_list = List.objects.get(pk=pk)

            choices = random.choices(
                rooms,
                weights=None,
                cum_weights=None,
                k=random.randint(min_count, max_count),
            )
            print(choices, type(choices))
            my_list.rooms.add(*choices)
            # to_add = rooms[start_position:end_position]
            # my_list.rooms.add(*to_add)

        self.stdout.write(
            self.style.SUCCESS(
                f"{number} list{number>1 and 's' or ''} are succefully made."
            )
        )

