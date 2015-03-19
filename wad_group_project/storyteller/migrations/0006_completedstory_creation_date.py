# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storyteller', '0005_auto_20150317_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedstory',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 15, 50, 32, 436000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
