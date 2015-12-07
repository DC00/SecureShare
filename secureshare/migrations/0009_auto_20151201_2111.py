# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureshare', '0008_message_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='uploaded_files',
            field=models.FileField(default=None, upload_to=b'uploads/', blank=True),
        ),
    ]
