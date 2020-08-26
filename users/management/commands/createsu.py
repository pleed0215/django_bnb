from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command will make super user."

    def handle(self, *args, **options):
        ebadmin = User.objects.get_or_none("ebadmin")

        if ebadmin is None:
            User.objects.create_superuser(
                "ebadmin", "admin@wbwoori.co.kr", "wbwoori0011!")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser created"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Superuser already existed"
                )
            )
