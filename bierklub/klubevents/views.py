from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Event, Member


def index(request):
    latest = Event.objects.order_by('-published_date')[:5]

    context = {
        'latest_event_list': latest,
    }

    return render(request, 'events/index.html', context)


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    return render(request, 'events/detail.html', {'event': event})


def attending(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    return render(request, 'events/attending.html', {'event': event})


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
