# Generated by Django 5.0.4 on 2024-04-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_gameroom_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_creator',
            field=models.BooleanField(default=True),
        ),
    ]
