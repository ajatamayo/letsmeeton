from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',

    url(r'^$', views.HomepageView.as_view(), name='home'),
)
