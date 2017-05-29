from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Event, Member


class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'

    def get_queryset(self):
        """Return the last 5 published events."""
        return Event.objects.order_by('-published_date')[:5]


class DetailView(generic.DetailView):
    model = Event
    template_name = 'events/detail.html'


class AttendingView(generic.DetailView):
    model = Event
    template_name = 'events/attending.html'


def attending_submit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    email = request.POST.get('email')
    name = request.POST.get('name')

    if not name or not email:
        return render(request, 'events/attending.html', {
            'event': event,
            'error_message': 'You must fill out all fields.',
            'name': name,
            'email': email,
        })

    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        member = Member(email=email, name=name)
        member.save()

    event.attendees.add(member)
    event.save()

    return HttpResponseRedirect(reverse('klubevents:attending_success',
                                        args=(event.id, member.id)))


def attending_success(request, event_id, member_id):
    event = get_object_or_404(Event, pk=event_id)
    member = get_object_or_404(Member, pk=member_id)

    return render(request, 'events/attending_success.html', {
        'event': event,
        'member': member
    })
