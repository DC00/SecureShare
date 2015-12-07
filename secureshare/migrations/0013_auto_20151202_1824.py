# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0012_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='uploaded_files',
            field=models.FileField(default=None, upload_to=django.core.files.storage.FileSystemStorage(location=b'/media/uploads'), blank=True),
        ),
    ]
