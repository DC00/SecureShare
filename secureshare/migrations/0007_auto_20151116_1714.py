# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0006_auto_20151116_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporter',
            name='timestamp',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
