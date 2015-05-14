# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0012_transaction_blocked_merchant'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='transactions',
            field=models.IntegerField(default=0),
        ),
    ]
