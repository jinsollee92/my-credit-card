# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc', '0002_auto_20150422_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.IntegerField()),
                ('zip', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('country', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_city',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_country',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_state',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='merchant_zip',
        ),
    ]
