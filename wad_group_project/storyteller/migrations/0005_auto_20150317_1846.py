# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storyteller', '0004_auto_20150304_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rater',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='story',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.AddField(
            model_name='category',
            name='stories',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedstory',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ongoingstory',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 17, 18, 46, 48, 315000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
