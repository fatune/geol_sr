# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('front_text', models.TextField()),
                ('back_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('explanation', models.TextField(default='')),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('memory_strength', models.FloatField(default=0)),
                ('last_answered', models.DateTimeField(auto_now_add=True)),
                ('to_be_answered', models.DateTimeField(default=None, blank=True, null=True)),
                ('card', models.ForeignKey(to='sr.Card')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='fact',
            name='subject',
            field=models.ForeignKey(to='sr.Subject'),
        ),
        migrations.AddField(
            model_name='card',
            name='fact',
            field=models.ForeignKey(to='sr.Fact'),
        ),
    ]
