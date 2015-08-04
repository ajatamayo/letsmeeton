# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='time_of_day',
            field=models.CharField(default='afternoon', max_length=16, choices=[(b'afternoon', b'Afternoon'), (b'evening', b'Evening')]),
            preserve_default=False,
        ),
    ]
