# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handicaps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='handicap_rounded',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
