# Generated by Django 4.2.3 on 2023-08-03 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_modality_remove_competition_type_modality_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='awards',
        ),
        migrations.RemoveField(
            model_name='competition',
            name='rules_and_regulations',
        ),
        migrations.RemoveField(
            model_name='season',
            name='competition',
        ),
        migrations.RemoveField(
            model_name='season',
            name='modality',
        ),
        migrations.AddField(
            model_name='competition',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='date_start',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='genre',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('MF', 'Mixed')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='number_grups',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.season'),
        ),
        migrations.AddField(
            model_name='competition',
            name='type_competition',
            field=models.CharField(choices=[('L', 'League'), ('T', 'Tournament'), ('P', 'Playoff'), ('F', 'Friendly'), ('GS', 'Group Stage'), ('O', 'Other')], default='O', max_length=2),
        ),
        migrations.AlterField(
            model_name='competition',
            name='sport',
            field=models.CharField(choices=[('F', 'Football'), ('B', 'Basketball'), ('V', 'Volleyball'), ('H', 'Handball'), ('T', 'Tennis'), ('O', 'Other')], default='O', max_length=1),
        ),
        migrations.DeleteModel(
            name='Modality',
        ),
    ]