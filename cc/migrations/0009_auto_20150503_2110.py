# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0008_remove_transaction_safe'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='mean',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='stdev',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='variance',
            field=models.FloatField(default=0),
        ),
    ]
