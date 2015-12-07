# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0003_auto_20151128_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='groups_that_can_view',
            field=models.ManyToManyField(related_name='groups_to', null=True, to='secureshare.Reporter', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='reporters_that_can_view',
            field=models.ManyToManyField(related_name='reporter_to', null=True, to='secureshare.Reporter', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(related_name='belongs_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
    ]
