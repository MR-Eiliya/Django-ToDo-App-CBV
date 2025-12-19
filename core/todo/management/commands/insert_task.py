from django.core.management.base import BaseCommand
from faker import Faker
from todo.models import Task
from accounts.models import CustomUserModel as User ,Profile
import random
from datetime import datetime


class Command(BaseCommand):
    help = "Inserting tasks with random status"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()


    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), 
                                        username=self.fake.unique.user_name(),
                                        password="usr/@1234567"
                                        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for _ in range(5):
            Task.objects.create(
                user = user,
                title=' '.join(self.fake.words(nb=3, unique=True)),
                is_completed = random.choice([True,False]),
                updated_date = datetime.now()
            )