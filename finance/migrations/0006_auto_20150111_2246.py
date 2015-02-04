# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20150111_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='backend_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
