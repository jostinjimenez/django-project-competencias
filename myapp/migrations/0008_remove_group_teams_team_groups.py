# Generated by Django 4.2.3 on 2023-08-06 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_group_letter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='teams',
        ),
        migrations.AddField(
            model_name='team',
            name='groups',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='myapp.group'),
        ),
    ]