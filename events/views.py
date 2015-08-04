from datetime import timedelta
from decimal import Decimal

from django.db.models import Prefetch
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Event, Signup


class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        today = timezone.now().date()

        try:
            event = Event.objects.prefetch_related(Prefetch(
                'signup_set',
                queryset=Signup.objects.filter(date__gte=today),
                to_attr='signups'
            )).latest('id')
        except Event.DoesNotExist:
            return context

        next_seven_days = {}
        for x in range(0, 7):
            for timeofday in Signup.TIMEOFDAY_CHOICES:
                day = today + timedelta(days=x)
                key = '%s|%s' % (day.strftime('%Y-%m-%d'), timeofday[0])
                next_seven_days[key] = {
                    'items': [],
                    'date': day,
                    'timeofday': timeofday[0],
                }

        for signup in event.signups:
            key = '%s|%s' % (signup.date.strftime('%Y-%m-%d'),
                             signup.time_of_day)
            next_seven_days[key]['items'].append(signup)

        next_seven_days = list(next_seven_days.iteritems())
        next_seven_days.sort()

        signup_width = Decimal(100) / event.target_number_of_attendees
        signup_width = round(signup_width, 2)

        context['event'] = event
        context['next_seven_days'] = next_seven_days
        context['signup_width'] = signup_width

        return context
