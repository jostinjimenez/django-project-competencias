# Generated by Django 4.2.3 on 2023-07-25 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_player_unique_together_playerteamseason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sport_images/'),
        ),
    ]
