# Generated by Django 4.2.3 on 2023-08-11 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_merge_20230811_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='myapp.season'),
        ),
    ]