import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as rooms_models
from users.models import User
from config.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = "This command will seed amenities for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--numbers",
            default=50,
            type=int,
            help="How many dummy rooms do you want make?",
        )

    def handle(self, *args, **options):
        how_many_rooms = options.get("numbers", 1)
        seeder = Seed.seeder()

        all_users = User.objects.all()
        room_types = rooms_models.RoomType.objects.all()
        amenities = rooms_models.Amenity.objects.all()
        facilities = rooms_models.Facility.objects.all()
        rules = rooms_models.HouseRule.objects.all()

        seeder.add_entity(
            rooms_models.Room,
            how_many_rooms,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 500),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )

        # 개중요.
        created_rooms_list = seeder.execute()
        list_cleaned = flatten(list(created_rooms_list.values()))

        for pk in list_cleaned:
            room = rooms_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(6, 10)):
                rooms_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    image=f"{MEDIA_ROOT}room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                fifty_fifty = random.randint(0, 100)
                if fifty_fifty % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                fifty_fifty = random.randint(0, 100)
                if fifty_fifty % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                fifty_fifty = random.randint(0, 100)
                if fifty_fifty % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(
            self.style.SUCCESS(f"{how_many_rooms} rooms succefully made.")
        )

