# Generated by Django 5.1.1 on 2024-10-27 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_customgpt_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='gpt',
            field=models.CharField(blank=True, default='main', max_length=100, null=True),
        ),
    ]