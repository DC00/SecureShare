# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0011_auto_20151201_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('contents', models.ManyToManyField(to='secureshare.Report', null=True, blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True)),
            ],
        ),
    ]
