from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command will make several rooms for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            default=50,
            type=int,
            help="How many dummy rooms do you want make?",
        )

    def handle(self, *args, **options):
        times = options.get("times")
        self.stdout.write(self.style.SUCCESS(f"{times} rooms succefully made."))

