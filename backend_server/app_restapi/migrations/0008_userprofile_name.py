# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2021-02-23 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_restapi', '0007_auto_20210224_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
