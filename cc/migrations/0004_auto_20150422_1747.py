# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0003_auto_20150422_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='merchant_id',
            field=models.ForeignKey(to='cc.Merchant', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='merchant_id',
            field=models.CharField(max_length=10),
        ),
    ]
