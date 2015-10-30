# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-10-15 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_event_invitations_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='externinscription',
            name='payment_mean',
            field=models.CharField(blank=True, choices=[('cash', 'Espèces'), ('check', 'Chèque'), ('card', 'Carte de crédit')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='inscription',
            name='payment_mean',
            field=models.CharField(blank=True, choices=[('cash', 'Espèces'), ('check', 'Chèque'), ('card', 'Carte de crédit')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='payment_mean',
            field=models.CharField(blank=True, choices=[('cash', 'Espèces'), ('check', 'Chèque'), ('card', 'Carte de crédit')], max_length=10, null=True),
        ),
    ]
