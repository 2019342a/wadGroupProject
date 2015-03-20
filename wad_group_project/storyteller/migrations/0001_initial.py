# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('stories', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompletedStory',
            fields=[
                ('completed_story_id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('views', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=128)),
                ('creator', models.CharField(max_length=128)),
                ('story_text', models.TextField()),
                ('slug', models.SlugField()),
                ('rating', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
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
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(to='storyteller.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=None)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
