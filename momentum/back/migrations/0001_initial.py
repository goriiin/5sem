# Generated by Django 5.1.2 on 2024-10-21 20:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=32, unique=True)),
                ('used_times', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('avatar_path', models.ImageField(default='default.jpg', upload_to='images')),
                ('answers_count', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('likes_count', models.IntegerField(default=0)),
                ('answers_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='back.profile')),
                ('tags', models.ManyToManyField(related_name='questions', to='back.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('correct', models.BooleanField(default=False)),
                ('likes_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='back.profile')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back.question')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.answer')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.profile')),
            ],
            options={
                'unique_together': {('user_id', 'answer')},
            },
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.profile')),
            ],
            options={
                'unique_together': {('question_id', 'user_id')},
            },
        ),
    ]
