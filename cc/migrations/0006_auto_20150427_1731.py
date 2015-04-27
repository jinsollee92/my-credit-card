# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0005_auto_20150427_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='card_number',
            field=models.CharField(serialize=False, max_length=16, primary_key=True, validators=[django.core.validators.RegexValidator(code='nomatch', regex='^.{16}$', message='Must be 16 digits')]),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='merchant_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='card_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(code='nomatch', regex='^.{16}$', message='Must be 16 digits')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
