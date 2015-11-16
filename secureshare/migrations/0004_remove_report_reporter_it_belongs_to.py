# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0003_auto_20151116_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='reporter_it_belongs_to',
        ),
    ]
