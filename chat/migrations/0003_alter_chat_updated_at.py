# Generated by Django 5.1.1 on 2024-09-30 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]