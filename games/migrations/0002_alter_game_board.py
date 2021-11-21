# Generated by Django 3.2.9 on 2021-11-21 17:42

import django.contrib.postgres.fields
from django.db import migrations, models
import games.models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='board',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), size=3), default=games.models.default_board, size=3),
        ),
    ]
