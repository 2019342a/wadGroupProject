# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompletedStory',
            fields=[
                ('completed_story_id', models.AutoField(serialize=False, primary_key=True)),
                ('views', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=128)),
                ('creator', models.CharField(max_length=128)),
                ('story_text', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='storyteller.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OngoingStory',
            fields=[
                ('ongoing_story_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('creator', models.CharField(max_length=128)),
                ('story_text', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='storyteller.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('age', models.IntegerField(default=None)),
                ('email', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(to='storyteller.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rating',
            name='story',
            field=models.ForeignKey(to='storyteller.CompletedStory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ongoingstory',
            name='users',
            field=models.ManyToManyField(to='storyteller.User'),
            preserve_default=True,
        ),
    ]
