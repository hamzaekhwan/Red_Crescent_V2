# Generated by Django 3.2.15 on 2022-12-30 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_person_reduce_shift_res_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='res_done',
            name='person_rank',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
