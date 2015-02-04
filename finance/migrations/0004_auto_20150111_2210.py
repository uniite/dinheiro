# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_account_backend_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(b'^\\d+$', b'Must be a number')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('institution', 'backend_id')]),
        ),
    ]
