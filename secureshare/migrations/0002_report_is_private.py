# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]
