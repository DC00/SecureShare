# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='uploaded_files',
            field=models.FileField(default=None, upload_to=b''),
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
