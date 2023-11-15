from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Tag, UserProfile, Question, Answer, Like
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Fill factor ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']

        self.stdout.write(self.style.SUCCESS('Filling the database...'))

        # Create users
        for _ in range(ratio):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(username=username, email=email, password=password)

        # Create tags
        for _ in range(ratio):
            Tag.objects.bulk_create(name=fake.word())

        # Create UserProfile and link to users
        for user in User.objects.all():
            UserProfile.objects.bulk_create(user=user, bio=fake.text())

        # Create questions
        for _ in range(ratio * 10):
            title = fake.sentence()
            content = fake.paragraph()
            user = random.choice(User.objects.all())
            question = Question.objects.bulk_create(title=title, content=content, user=user)

            # Add tags to questions
            tags = random.sample(list(Tag.objects.all()), random.randint(1, ratio))
            question.tags.add(*tags)

            # Create answers
            for _ in range(ratio * 100):
                content = fake.paragraph()
                Answer.objects.bulk_create(content=content, question=question, user=random.choice(User.objects.all()))

            # Create likes
            for _ in range(ratio * 200):
                user = random.choice(User.objects.all())
                like = Like.objects.bulk_create(user=user, question=question)
                if random.choice([True, False]):
                    like.answer = random.choice(Answer.objects.filter(question=question))
                    like.save()

        self.stdout.write(self.style.SUCCESS(f'Database filled with data for ratio: {ratio}'))