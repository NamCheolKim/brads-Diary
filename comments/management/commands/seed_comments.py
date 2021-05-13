import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from comments import models as comment_models
from users import models as user_models
from diarys import models as diary_models


class Command(BaseCommand):
    help = "This command created many post"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many comment do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        postdiary = diary_models.PostDiary.objects.all()
        seeder.add_entity(
            comment_models.Comment,
            number,
            {
                "diary": lambda x: random.choice(postdiary),
                "user": lambda x: random.choice(users),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} comment created."))
