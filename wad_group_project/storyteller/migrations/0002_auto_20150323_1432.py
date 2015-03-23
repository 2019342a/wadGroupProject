# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storyteller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ongoingstory',
            name='contributors',
            field=models.ManyToManyField(related_name='contributorlist', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ongoingstory',
            name='ended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ongoingstory',
            name='ending',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ongoingstory',
            name='votes_to_end',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
