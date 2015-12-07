# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0002_auto_20151203_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporter',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
