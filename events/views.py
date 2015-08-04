from django.views.generic import TemplateView

from .models import Event


class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        try:
            event = Event.objects.latest('id')
        except Event.DoesNotExist:
            event = None

        context['event'] = event
        return context
