# Generated by Django 3.2.15 on 2023-02-12 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_reservations_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations_time',
            name='max_person',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
