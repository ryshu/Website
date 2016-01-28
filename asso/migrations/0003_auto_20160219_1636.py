# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asso', '0002_auto_20160217_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asso',
            options={'permissions': (('manage_asso', 'Can manage associations'),)},
        ),
        migrations.AlterField(
            model_name='asso',
            name='admins_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='asso_admin_set', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='asso',
            name='members_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='asso_set', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='asso',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
