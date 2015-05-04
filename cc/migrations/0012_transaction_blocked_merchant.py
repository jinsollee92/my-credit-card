# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0011_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='blocked_merchant',
            field=models.BooleanField(default=False),
        ),
    ]
