# Generated by Django 5.0.4 on 2024-04-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_player_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_turn',
            field=models.BooleanField(default=False),
        ),
    ]
