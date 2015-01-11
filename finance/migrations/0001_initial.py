# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_number', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(b'^\\d+$', b'Must be a number')])),
                ('name', models.CharField(max_length=50, blank=True)),
                ('routing_number', models.CharField(blank=True, max_length=9, validators=[django.core.validators.RegexValidator(b'^\\d+$', b'Must be a number')])),
                ('balance', models.DecimalField(default=0, max_digits=15, decimal_places=2)),
                ('broker_id', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(blank=True, to='finance.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'contains', max_length=10, choices=[(b'contains', b'Contains'), (b'startswith', b'Starts With'), (b'endswith', b'Ends With')])),
                ('field', models.CharField(default=b'payee', max_length=20, choices=[(b'date', b'Date'), (b'payee', b'Payee'), (b'type', b'Type')])),
                ('content', models.TextField()),
                ('category', models.ForeignKey(related_name='rules', to='finance.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fid', models.IntegerField()),
                ('org', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('name', models.CharField(default=b'Unknown', max_length=255)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=15, decimal_places=2)),
                ('currency', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z]+$')])),
                ('date', models.DateTimeField()),
                ('payee', models.CharField(max_length=255)),
                ('transaction_id', models.CharField(max_length=255)),
                ('mcc', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('memo', models.TextField(blank=True)),
                ('sic', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('type', models.CharField(max_length=50, blank=True)),
                ('account', models.ForeignKey(to='finance.Account')),
                ('category', models.ForeignKey(blank=True, to='finance.Category', null=True)),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('account', 'transaction_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='institution',
            unique_together=set([('fid', 'username')]),
        ),
        migrations.AddField(
            model_name='account',
            name='institution',
            field=models.ForeignKey(to='finance.Institution'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('institution', 'account_number')]),
        ),
    ]
