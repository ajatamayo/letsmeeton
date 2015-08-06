from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import redirect
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

        context['event'] = event

        if not self.request.user.is_authenticated():
            context['form'] = AuthenticationForm()
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

            if signup.attendee == self.request.user:
                next_seven_days[key]['attending'] = True

        next_seven_days = list(next_seven_days.iteritems())
        next_seven_days.sort()

        signup_width = Decimal(100) / event.target_number_of_attendees
        signup_width = round(signup_width, 2)

        context['next_seven_days'] = next_seven_days
        context['signup_width'] = signup_width

        n = event.target_number_of_attendees
        context['alphas'] = [1.0 / n * x for x in range(1, n + 1)]

        return context

    def post(self, request, *args, **kwargs):
        if '_login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return redirect('home')

        if '_logout' in request.POST:
            logout(request)
            return redirect('home')

        if 'signup' in request.POST:
            Signup.objects.filter(pk=request.POST['signup']).delete()
            return JsonResponse({'status': 'deleted'})

        try:
            event = Event.objects.latest('id')
        except Event.DoesNotExist:
            return JsonResponse({'status': 'noevent'})

        if 'date' in request.POST and 'timeofday' in request.POST:
            signup = Signup.objects.create(
                event=event,
                attendee=request.user,
                date=request.POST['date'],
                time_of_day=request.POST['timeofday'])
            signup_width = Decimal(100) / event.target_number_of_attendees
            signup_width = round(signup_width, 2)
            return JsonResponse({
                'status': 'confirmed',
                'signup': signup.pk,
                'width': signup_width,
            })

        return JsonResponse({'status': 'fail'})
