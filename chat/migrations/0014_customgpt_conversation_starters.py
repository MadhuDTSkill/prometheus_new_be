# Generated by Django 5.1.1 on 2024-10-27 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_chat_gpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgpt',
            name='conversation_starters',
            field=models.JSONField(default=list),
        ),
    ]
