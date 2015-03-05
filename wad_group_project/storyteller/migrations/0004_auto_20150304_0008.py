# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyteller', '0003_auto_20150304_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedstory',
            name='slug',
            field=models.SlugField(),
        ),
    ]
