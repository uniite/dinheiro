# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='ofx_token',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
