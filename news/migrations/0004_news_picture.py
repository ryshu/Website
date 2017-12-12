# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_comment_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='news_pictures'),
        ),
    ]
