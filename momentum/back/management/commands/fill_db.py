from django.core.management.base import BaseCommand
from back.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike
from django.contrib.auth.models import User
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Create users and profiles in bulk
        users = [User(username=fake.user_name() + f"{i}", email=f"{i}" + fake.email(), password='123') for i in
                 range(ratio)]
        User.objects.bulk_create(users)

        profiles = [Profile(user=user) for user in User.objects.all()]
        Profile.objects.bulk_create(profiles)

        # Create tags in bulk
        tags = set()  # Используем множество для хранения уникальных имен тегов
        existing_tags = set(Tag.objects.values_list('tag_name', flat=True))  # Существующие теги в базе данных

        while len(tags) < ratio:
            name = fake.word()
            if name not in existing_tags:  # Проверяем, существует ли тег
                tags.add(name)  # Добавляем только уникальные имена тегов

        # Создаем объекты Tag и сохраняем их в bulk
        tag_objects = [Tag(tag_name=name) for name in tags]
        Tag.objects.bulk_create(tag_objects)

        # Create questions in bulk
        profiles = list(Profile.objects.all())  # Retrieve profiles once to avoid querying in the loop
        questions = []
        for i in range(ratio * 10):
            profile = random.choice(profiles)
            questions.append(Question(title=fake.sentence(), content=fake.paragraph(), author=profile))
        Question.objects.bulk_create(questions)

        # Add tags to questions
        questions = list(Question.objects.all())
        tags = list(Tag.objects.all())
        for question in questions:
            random_tags = random.sample(tags, random.randint(1, 5))  # Select random 1 to 5 tags per question
            question.tags.set(random_tags)

        # Create answers in bulk
        answers = []
        for i in range(ratio * 100):
            question = random.choice(questions)
            profile = random.choice(profiles)
            answers.append(Answer(answer=fake.paragraph(), question=question, author=profile, correct=fake.boolean()))
        Answer.objects.bulk_create(answers)

        # Create question likes in bulk with uniqueness check
        question_likes_set = set()
        question_likes = []
        for i in range(ratio * 200):
            question = random.choice(questions)
            profile = random.choice(profiles)
            key = (question.id, profile.id)
            if key not in question_likes_set:
                question_likes_set.add(key)
                vote = random.choice([-1, 1])
                question_likes.append(QuestionLike(user_id=profile, question_id=question, vote=vote))
        QuestionLike.objects.bulk_create(question_likes)

        # Create answer likes in bulk with uniqueness check
        answer_likes_set = set()
        answer_likes = []
        for i in range(ratio * 200):
            answer = random.choice(answers)
            profile = random.choice(profiles)
            key = (answer.id, profile.id)
            if key not in answer_likes_set:
                answer_likes_set.add(key)
                vote = random.choice([-1, 1])
                answer_likes.append(AnswerLike(user_id=profile, answer_id=answer, vote=vote))
        AnswerLike.objects.bulk_create(answer_likes)

        self.stdout.write(self.style.SUCCESS(f'Database filled with {ratio}x data'))
