# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('uploaded_files', models.FileField(upload_to='', default=None)),
            ],
        ),
    ]
