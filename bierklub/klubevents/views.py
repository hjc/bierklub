from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Event, Member


def index(request):
    latest = Event.objects.order_by('-published_date')[:5]

    context = {
        'latest_event_list': latest,
    }

    return render(request, 'events/index.html', context)
