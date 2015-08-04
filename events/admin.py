from django.contrib import admin

from .models import Event, Signup


class EventAdmin(admin.ModelAdmin):
    '''
        Admin View for Event
    '''
    list_display = ('name', 'target_number_of_attendees',)
    search_fields = ['name']

admin.site.register(Event, EventAdmin)


class SignupAdmin(admin.ModelAdmin):
    '''
        Admin View for Signup
    '''
    list_display = ('event', 'attendee', 'date', 'time_of_day',)
    search_fields = ['event', 'attendee']

admin.site.register(Signup, SignupAdmin)
