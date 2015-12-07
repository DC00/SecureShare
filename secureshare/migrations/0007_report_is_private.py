# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0006_auto_20151130_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
