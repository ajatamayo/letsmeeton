# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_signup_time_of_day'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='signup',
            unique_together=set([('event', 'attendee', 'date', 'time_of_day')]),
        ),
    ]
