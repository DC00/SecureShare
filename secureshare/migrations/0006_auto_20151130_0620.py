# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0005_remove_report_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='groups_that_can_view',
            field=models.ManyToManyField(related_name='groups_to', null=True, to='secureshare.Group', blank=True),
        ),
    ]
