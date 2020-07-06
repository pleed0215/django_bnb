from django.core.management.base import BaseCommand
from users.models import User
from django_seed import Seed


class Command(BaseCommand):
    help = "This command will seed users for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=50,
            type=int,
            help="How many dummy users do you want make?",
        )

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        number = options.get("number", 1)
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False,})
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(
                f"{number} user{number>1 and 's' or ''} that are no admin or staff succefully made."
            )
        )

