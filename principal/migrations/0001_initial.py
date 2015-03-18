# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import principal.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'administrator',
                'permissions': (('administrator', 'Administrator'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'assessment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_foursquare', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'city',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoinHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(validators=[principal.models.PastValidator])),
                ('concept', models.TextField()),
            ],
            options={
                'db_table': 'coin_history',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numberDay', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('date', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'day',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True)),
                ('leadTime', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('duration', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('usefulCount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
            options={
                'db_table': 'feedback',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Judges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'judges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('useful', models.BooleanField(default=False)),
                ('comment', models.TextField(null=True)),
                ('feedback', models.ForeignKey(to='principal.Feedback')),
            ],
            options={
                'db_table': 'likes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('date', models.DateTimeField(validators=[principal.models.PastValidator])),
            ],
            options={
                'db_table': 'payment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('openingTime', models.CharField(max_length=128, null=True)),
                ('closingTime', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'schedule',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scorable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('rating', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'db_table': 'scorable',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Traveller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=2, choices=[(b'MA', b'MALE'), (b'FE', b'FEMALE')])),
                ('photo', models.ImageField(null=True, upload_to=b'static/user_folder/', blank=True)),
                ('reputation', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('coins', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('recommendations', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'db_table': 'traveller',
                'permissions': (('traveller', 'Traveller'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('scorable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='principal.Scorable')),
                ('publishedDescription', models.TextField(null=True)),
                ('startDate', models.DateField(null=True)),
                ('endDate', models.DateField(null=True)),
                ('planified', models.BooleanField(default=False)),
                ('coins', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('likes', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('dislikes', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('city', models.ForeignKey(to='principal.City')),
                ('traveller', models.ForeignKey(to='principal.Traveller')),
            ],
            options={
                'db_table': 'trip',
            },
            bases=('principal.scorable',),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('scorable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='principal.Scorable')),
                ('id_foursquare', models.CharField(unique=True, max_length=30)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('photo', models.ImageField(null=True, upload_to=b'static/venue_folder/', blank=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('categories', models.ManyToManyField(to='principal.Category')),
            ],
            options={
                'db_table': 'venue',
            },
            bases=('principal.scorable',),
        ),
        migrations.CreateModel(
            name='VenueDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('day', models.ForeignKey(to='principal.Day')),
                ('venue', models.ForeignKey(to='principal.Venue')),
            ],
            options={
                'db_table': 'venue_day',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='venueday',
            unique_together=set([('venue', 'day')]),
        ),
        migrations.AddField(
            model_name='traveller',
            name='assessedScorables',
            field=models.ManyToManyField(to='principal.Scorable', through='principal.Assessment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='traveller',
            name='commentedTrips',
            field=models.ManyToManyField(related_name='commenters', through='principal.Comment', to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='traveller',
            name='jugedTrips',
            field=models.ManyToManyField(related_name='judges', through='principal.Judges', to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='traveller',
            name='likedFeedback',
            field=models.ManyToManyField(related_name='traveller_likes', through='principal.Likes', to='principal.Feedback'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='traveller',
            name='user_account',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='venue',
            field=models.ForeignKey(to='principal.Venue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='likes',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judges',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judges',
            name='trip',
            field=models.ForeignKey(related_name='judgedTrip', to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='venues',
            field=models.ForeignKey(to='principal.Venue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='day',
            name='trip',
            field=models.ForeignKey(to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='day',
            name='venues',
            field=models.ManyToManyField(to='principal.Venue', through='principal.VenueDay'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='trip',
            field=models.ForeignKey(to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coinhistory',
            name='payment',
            field=models.OneToOneField(null=True, blank=True, to='principal.Payment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coinhistory',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coinhistory',
            name='trip',
            field=models.OneToOneField(null=True, blank=True, to='principal.Trip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessment',
            name='scorable',
            field=models.ForeignKey(to='principal.Scorable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessment',
            name='traveller',
            field=models.ForeignKey(to='principal.Traveller'),
            preserve_default=True,
        ),
    ]
