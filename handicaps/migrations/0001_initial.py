# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='GameScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('game', models.ForeignKey(to='handicaps.Game')),
            ],
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('level_4', models.IntegerField()),
                ('level_4_result', models.DecimalField(max_digits=2, decimal_places=1)),
                ('level_3_min', models.IntegerField()),
                ('level_3_max', models.IntegerField()),
                ('level_3_result', models.DecimalField(max_digits=2, decimal_places=1)),
                ('level_2_min', models.IntegerField()),
                ('level_2_max', models.IntegerField()),
                ('level_2_result', models.DecimalField(max_digits=2, decimal_places=1)),
                ('level_1', models.IntegerField()),
                ('level_1_result', models.DecimalField(max_digits=2, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade_use', models.IntegerField(default=3, choices=[(3, b'3 grades'), (4, b'4 grades'), (5, b'5 grades')])),
                ('grade_a_min', models.IntegerField(default=0)),
                ('grade_a_max', models.IntegerField(default=0)),
                ('grade_b_min', models.IntegerField(default=0)),
                ('grade_b_max', models.IntegerField(default=0)),
                ('grade_c_min', models.IntegerField(default=0)),
                ('grade_c_max', models.IntegerField(default=0)),
                ('grade_d_min', models.IntegerField(default=0)),
                ('grade_d_max', models.IntegerField(default=0)),
                ('grade_e_min', models.IntegerField(default=0)),
                ('grade_e_max', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('handicap', models.DecimalField(max_digits=3, decimal_places=1)),
                ('latest_handicap_change', models.DecimalField(null=True, max_digits=2, decimal_places=1)),
                ('latest_game', models.DateField(null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='gamescore',
            name='player',
            field=models.ForeignKey(to='handicaps.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.ForeignKey(to='handicaps.GameType'),
        ),
    ]
