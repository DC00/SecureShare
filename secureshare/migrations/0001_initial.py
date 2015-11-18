# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('uploaded_files', models.FileField(upload_to='', default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(to='secureshare.Reporter', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
