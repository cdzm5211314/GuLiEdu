# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-29 10:55
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orginfo',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='机构详情'),
        ),
    ]
