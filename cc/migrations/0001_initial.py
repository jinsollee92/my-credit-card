# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.IntegerField(primary_key=True, serialize=False)),
                ('merchant_id', models.IntegerField()),
                ('merchant_zip', models.CharField(max_length=5)),
                ('merchant_city', models.CharField(max_length=50)),
                ('merchant_state', models.CharField(max_length=2)),
                ('merchant_country', models.CharField(max_length=50)),
                ('merchant_name', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('safe', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('card_number', models.CharField(primary_key=True, serialize=False, max_length=16)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('zip', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='card_number',
            field=models.ForeignKey(to='cc.User'),
        ),
    ]
