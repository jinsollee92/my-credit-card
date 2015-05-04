# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0010_auto_20150503_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('customer', models.ForeignKey(to='cc.Customer')),
                ('merchant', models.ForeignKey(to='cc.Merchant')),
            ],
        ),
    ]
