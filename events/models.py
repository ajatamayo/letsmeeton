from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    target_number_of_attendees = models.PositiveIntegerField(default=2)

    def __unicode__(self):
        return u'%s' % self.name


class Signup(models.Model):
    AFTERNOON = 'afternoon'
    EVENING = 'evening'
    TIMEOFDAY_CHOICES = (
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
    )
    event = models.ForeignKey('events.Event')
    attendee = models.ForeignKey('auth.User')
    date = models.DateField()
    time_of_day = models.CharField(max_length=16, choices=TIMEOFDAY_CHOICES)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.event,
                                 self.attendee,
                                 self.date.strftime('%Y-%m-%d'),
                                 self.get_time_of_day_display())
