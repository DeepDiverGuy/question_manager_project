import random
from faker import Faker
from question_manager.models import Question

fake = Faker()

def run():
    total_questions = 100
    for _ in range(total_questions):
        question = Question(
            question=fake.sentence(),
            option1=fake.sentence(),
            option2=fake.sentence(),
            option3=fake.sentence(),
            option4=fake.sentence(),
            option5=fake.sentence(),
            answer=random.randint(1, 5),  # Random answer option (1 to 5)
            explain=fake.paragraph()
        )
        question.save()

