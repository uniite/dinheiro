# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20150111_2210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='account_number',
            new_name='number',
        ),
    ]
