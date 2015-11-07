# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('uploaded_files', models.FileField(upload_to='')),
            ],
        ),
    ]
