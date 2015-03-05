# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyteller', '0002_auto_20150303_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedstory',
            name='completed_story_id',
            field=models.AutoField(unique=True, serialize=False, primary_key=True),
        ),
    ]
