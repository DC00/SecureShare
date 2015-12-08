# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='secureshare.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(default=b'defualt Message')),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('uploaded_files', models.FileField(default=None, upload_to=b'')),
                ('is_private', models.BooleanField(default=False)),
                ('groups_that_can_view', models.ManyToManyField(related_name='groups_to', null=True, to='secureshare.Group', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=120, null=True)),
                ('password', models.CharField(max_length=120, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('is_superuser', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='reporter_it_belongs_to',
            field=models.ForeignKey(related_name='belongs_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='reporters_that_can_view',
            field=models.ManyToManyField(related_name='reporter_to', null=True, to='secureshare.Reporter', blank=True),
        ),
        migrations.AddField(
            model_name='message',
            name='send_to',
            field=models.ForeignKey(related_name='send_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sender', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='reporter',
            field=models.ForeignKey(to='secureshare.Reporter'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='secureshare.Reporter', through='secureshare.Membership'),
        ),
        migrations.AddField(
            model_name='folder',
            name='contents',
            field=models.ManyToManyField(to='secureshare.Report', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='secureshare.Reporter', null=True),
        ),
    ]
