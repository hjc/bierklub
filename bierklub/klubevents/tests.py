import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Event


class EventMethodTests(TestCase):
    def test_was_published_recently_with_future_event(self):
        """
        was_published_recently should return False for Events in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_event = Event(published_date=time)
        self.assertFalse(future_event.was_published_recently())

    def test_was_published_recently_with_past_event(self):
        """
        was_published_recently() should return False for Events whose Publish
        date is older  than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_event = Event(published_date=time)
        self.assertFalse(old_event.was_published_recently())

    def test_was_published_recently_with_recent_event(self):
        """
        was_published_recently() should return True for Events whose Publish
        Date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_event = Event(published_date=time)
        self.assertTrue(recent_event.was_published_recently())

    def test_is_soon_with_past_event(self):
        """
        is_soon() should return False for Events in the past.
        """
        time = timezone.now() - datetime.timedelta(days=7)
        past_event = Event(date=time)
        self.assertFalse(past_event.is_soon())

    def test_is_soon_out_of_range(self):
        """
        is_soon() should return False for events greater than week away.
        """
        time = timezone.now() + datetime.timedelta(days=8)
        future_event = Event(date=time)
        self.assertFalse(future_event.is_soon())

    def test_is_soon(self):
        """
        is_soon() should return True for events less than a week away, but in
        the future.
        """
        time = timezone.now() + datetime.timedelta(days=6)
        future_event = Event(date=time)
        self.assertTrue(future_event.is_soon())


def create_event(days=None, number=1, **kwargs):
    """Thin wrapper for creating and returning an Event.

    You can easily set the publication date to a day in the future by using the
    ``days`` kwarg, or you can set the date directly through the function
    kwargs.

    Pass all model attributes through kwargs.

    Kwargs:
        days (int): An integer number of days into the future. Use negative
            numbers for past dates.
        name (str): The name of the event.
        description (str): The description for the event.
        date (datetime): An exact date for when the event will occur.
        number (int): The number this event is, e.g., the 2nd event.
        location (str): Address of the event.
        attendees (list[klubevents.models.Member]): A list of members who will
            be attending this event.
        published_date (datetime): When this event should be published on the
            site; use either this or ``days``, but never both (``days`` will be
            preferred) .
        preamble (str): The intro text for the event.
        additional_notes (str): Markdown for the bottom section of the event
            writeup.

    Returns:
        klubevents.models.Event: A newly created and persisted Event model.
    """
    if days is not None:
        # cannot use both options here
        kwargs.pop('published_date', None)
        dt = timezone.now() + datetime.timedelta(days)
    else:
        dt = kwargs.pop('published_date', None)

    return Event.objects.create(number=number, published_date=dt, **kwargs)


class EventViewTestCase(TestCase):
    def test_index_view_with_no_events(self):
        """If no events exist, an appropriate message should be displayed.
        """
        resp = self.client.get(reverse('klubevents:index'))

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'No events are available.')
        self.assertQuerysetEqual(resp.context['latest_event_list'], [])

    def test_index_view_with_a_past_event(self):
        """Events with a published date in the past should be displayed on the
        page.
        """
        when = timezone.now() + datetime.timedelta(days=2)
        event = create_event(days=-1, name='Past Test',
                             description='Past Test', date=when,
                             location='123 Fake Street')
        resp = self.client.get(reverse('klubevents:index'))

        expected = ['<Event: Past Test at 123 Fake Street on {}>'.format(
            when.strftime('%Y-%m-%d')
        )]
        self.assertQuerysetEqual(
            resp.context['latest_event_list'],
            expected
        )

    def test_index_view_with_a_future_event(self):
        """Events published in the future should not be displayed on the index.
        """
        when = timezone.now() + datetime.timedelta(days=30)
        event = create_event(days=7, name='Future Test',
                             description='Future Test', date=when,
                             location='123 Fake Street')
        resp = self.client.get(reverse('klubevents:index'))

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'No events are available.')
        self.assertQuerysetEqual(resp.context['latest_event_list'], [])

    def test_index_view_with_future_and_past_event(self):
        """If there is an event published in the future and one published in
        the past, only show the one published in the past.
        """
        when = timezone.now() + datetime.timedelta(days=2)

        past_event = create_event(days=-1, name='Past Test',
                                  description='Past Test', date=when,
                                  location='123 Fake Street')
        future_event = create_event(days=7, name='Future Event',
                                    description='Future Test', date=when,
                                    location='123 Fake Street')
        resp = self.client.get(reverse('klubevents:index'))

        expected = ['<Event: Past Test at 123 Fake Street on {}>'.format(
            when.strftime('%Y-%m-%d')
        )]
        self.assertQuerysetEqual(
            resp.context['latest_event_list'],
            expected
        )

    def test_index_view_with_two_past_events(self):
        """The index page should display multiple events, if they were all
        published in the past.
        """
        expected = []
        for i in range(1, 3):
            when = timezone.now() + datetime.timedelta(days=i)
            create_event(days=-i, name='Past Test {}'.format(i),
                         description='Test', date=when,
                         location='123 Fake Street', number=i)
            expected.append(
                '<Event: Past Test {} at 123 Fake Street on {}>'.format(
                    i, when.strftime('%Y-%m-%d')
                )
            )

        resp = self.client.get(reverse('klubevents:index'))

        self.assertQuerysetEqual(resp.context['latest_event_list'], expected)

    def test_index_view_with_six_past_events(self):
        """The index page should only display the five most recent events.
        """
        expected = []

        for i in range(1, 7):
            when = timezone.now() + datetime.timedelta(days=i)
            create_event(days=-i, name='Past Test {}'.format(i),
                         description='Test', date=when,
                         location='123 Fake Street', number=i)

            # only the first 5 events are expected
            if i != 6:
                expected.append(
                    '<Event: Past Test {} at 123 Fake Street on {}>'.format(
                        i, when.strftime('%Y-%m-%d')
                    )
                )

        resp = self.client.get(reverse('klubevents:index'))
        self.assertQuerysetEqual(resp.context['latest_event_list'], expected)
