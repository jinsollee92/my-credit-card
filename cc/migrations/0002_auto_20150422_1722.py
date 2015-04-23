# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('card_number', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('zip', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='card_number',
            field=models.ForeignKey(to='cc.Customer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(max_length=10, serialize=False, primary_key=True),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
