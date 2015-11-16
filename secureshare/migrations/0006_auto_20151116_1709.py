# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0005_auto_20151116_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('group', models.ForeignKey(to='secureshare.Group')),
                ('reporter', models.ForeignKey(to='secureshare.Reporter')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('content', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('group_it_belongs_to', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(default=None, to='secureshare.Reporter'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='secureshare.Membership', to='secureshare.Reporter'),
        ),
    ]
