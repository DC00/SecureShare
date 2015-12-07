# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0002_auto_20151127_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sender', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='send_to',
            field=models.ForeignKey(related_name='send_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
    ]
