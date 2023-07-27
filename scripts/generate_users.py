import random
from faker import Faker
from question_manager.models import User

fake = Faker()

def run():
    total_users = 500

    for _ in range(total_users):
        user = User(
            idname=fake.unique.word(),
            display_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        user.save()
