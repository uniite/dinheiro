# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20150111_2246'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institution',
            unique_together=set([('owner', 'name')]),
        ),
        migrations.RemoveField(
            model_name='institution',
            name='username',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='url',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='password',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='org',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='fid',
        ),
    ]
