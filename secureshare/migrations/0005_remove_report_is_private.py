# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0004_auto_20151130_0554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_private',
        ),
    ]
