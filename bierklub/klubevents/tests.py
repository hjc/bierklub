import datetime

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
