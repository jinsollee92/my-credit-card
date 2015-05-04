# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0009_auto_20150503_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='safe_size',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='subscription',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='suspicious',
            field=models.BooleanField(default=False),
        ),
    ]
