# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('group', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('content', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('group_it_belongs_to', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('uploaded_files', models.FileField(upload_to='', default=None)),
                ('is_private', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='secureshare.Reporter', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='reporter',
            field=models.ForeignKey(to='secureshare.Reporter'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='secureshare.Membership', to='secureshare.Reporter'),
        ),
    ]
