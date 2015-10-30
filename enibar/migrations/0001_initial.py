# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-10-26 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('alcoholic', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoryLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('note', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('price_name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('nickname', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=254)),
                ('note', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PriceDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enibar.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enibar.Category')),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='description',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enibar.PriceDescription'),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enibar.Product'),
        ),
    ]
