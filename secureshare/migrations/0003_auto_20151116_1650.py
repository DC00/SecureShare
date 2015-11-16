# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0002_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('content', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('group_it_belongs_to', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='uploaded_files',
            field=models.FileField(upload_to='', default=None),
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
        migrations.AddField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(default=datetime.datetime(2015, 11, 16, 16, 50, 15, 335327, tzinfo=utc), to='secureshare.Reporter'),
            preserve_default=False,
        ),
    ]
