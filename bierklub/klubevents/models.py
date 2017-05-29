import datetime

from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=4096)
    date = models.DateTimeField()
    number = models.IntegerField('number IRT total events')
    location = models.CharField('address of brewery', max_length=128)
    attendees = models.ManyToManyField('Member',
                                       db_table='klubevents_event_members')
    published_date = models.DateTimeField('date event was created',
                                          default=timezone.now)
    preamble = models.CharField(max_length=512, default='')
    additional_notes = models.CharField(max_length=1024, default='')

    def __str__(self):
        return (self.name + ' at ' + self.location + ' on '
                + self.date.strftime('%Y-%m-%d'))

    def was_published_recently(self):
        """Was this event invite published on the site recently.

        NOTE: Has NOTHING to do with when the event will actually be, please
        see :meth:`is_soon` for that.

        Returns:
            bool: True if event was created within the past day.
        """
        recent = timezone.now() - datetime.timedelta(days=1)
        return self.published_date >= recent

    def is_soon(self):
        """Has the event happened yet and, if not, will it happen in a week.

        Returns:
            bool: Whether or not the event will happen in a week.
        """
        soon = timezone.now() + datetime.timedelta(days=7)
        now = timezone.now()
        return now < self.date <= soon


class Member(models.Model):
    name = models.CharField('full name', max_length=128)
    email = models.EmailField()
    join_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name + ' <' + self.email + '>'

