from django.conf.urls import url

from . import views


app_name = 'klubevents'
urlpatterns = [
    # ex: /events/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /events/5/
    url(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /events/5/attending/
    url(r'(?P<pk>[0-9]+)/attending/$', views.AttendingView.as_view(),
        name='attending'),
    url(r'(?P<event_id>[0-9]+)/attending/submit/$', views.attending_submit,
        name='attending_submit'),
    url(r'(?P<pk>[0-9]+)/attending/(?P<member_id>[0-9]+)',
        views.AttendingSuccessView.as_view(), name='attending_success'),
]
