from django.conf.urls import url

from . import views


app_name = 'klubevents'
urlpatterns = [
    # ex: /events/
    url(r'^$', views.index, name='index'),
    # ex: /events/5/
    url(r'(?P<event_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /events/5/attending/
    url(r'(?P<event_id>[0-9]+)/attending/$', views.attending,
        name='attending'),
    url(r'(?P<event_id>[0-9]+)/attending/submit/$', views.attending_submit,
        name='attending_submit'),
    url(r'(?P<event_id>[0-9]+)/attending/(?P<member_id>[0-9]+)',
        views.attending_success, name='attending_success'),
]
