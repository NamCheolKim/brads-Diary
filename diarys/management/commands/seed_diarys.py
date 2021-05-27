import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from diarys import models as diary_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command created many post"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many post do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        seeder.add_entity(
            diary_models.PostDiary,
            number,
            {"author": lambda x: random.choice(all_users)},
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Post create"))
