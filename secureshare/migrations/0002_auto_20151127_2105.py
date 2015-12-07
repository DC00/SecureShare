# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_private',
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(default=b'defualt Message'),
        ),
        migrations.AlterField(
            model_name='report',
            name='uploaded_files',
            field=models.FileField(default=None, upload_to=b'', blank=True),
        ),
    ]
