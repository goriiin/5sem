# Generated by Django 5.1.2 on 2024-11-12 23:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0003_remove_post_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='post_files/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='back.post')),
            ],
        ),
    ]
