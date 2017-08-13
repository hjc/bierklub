from django.conf.urls import url

from . import views
from .views.members import RegisterView


app_name = 'klubevents'
urlpatterns = [

    # ex: /events/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ex: /events/5/
    url(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # ex: /events/5/attending/
    url(r'(?P<pk>[0-9]+)/attending/$', views.AttendingView.as_view(),
        name='attending'),

    # ex: /events/5/attending/submit
    url(r'(?P<event_id>[0-9]+)/attending/submit/$', views.attending_submit,
        name='attending_submit'),

    # ex: events/5/attending/9
    url(r'(?P<pk>[0-9]+)/attending/(?P<member_id>[0-9]+)',
        views.AttendingSuccessView.as_view(), name='attending_success'),
    url(r'^register/$', RegisterView.as_view(), name='member_registration'),
]
