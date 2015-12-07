# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0007_report_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
