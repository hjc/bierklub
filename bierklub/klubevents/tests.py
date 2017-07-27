import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Event, Member

DEFAULT_MEMBER_NAME = 'Tom Hanks'
DEFAULT_MEMBER_EMAIL = 'tom.hanks@example.com'
DEFAULT_MEMBER_PASSWORD = 'password'


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


def create_member(name=DEFAULT_MEMBER_NAME, email=DEFAULT_MEMBER_EMAIL,
                  password=DEFAULT_MEMBER_PASSWORD):
    """Thin wrapper for creating and returning a Member.

    Calling it as is creates our Tommy Hanks.

    Kwargs:
        name (str): The name for the Member.
        email (str): The email for the member.

    Returns:
        klubevents.models.Member: The newly made Member.
    """
    first, last = name.split(' ')
    user = User.objects.create_user(email, email, password, first_name=first,
                                    last_name=last)
    member = Member(email=email, name=name, user=user)
    member.save()
    return member


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


class EventDetailTests(TestCase):
    def test_detail_with_future_event(self):
        """The detail view of an Event with a future published date should 404.
        """
        when = timezone.now() + datetime.timedelta(30)
        future_event = create_event(days=7, name='Future Test',
                                    description='Future Test', date=when,
                                    location='123 Fake Street')
        url = reverse('klubevents:detail', args=(future_event.id,))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_detail_with_past_event(self):
        """The detail view of an Event with a past published date should render.
        """
        when = timezone.now() + datetime.timedelta(7)
        past_event = create_event(days=-5, name='Past Test',
                                    description='Past Test', date=when,
                                    location='123 Fake Street')
        url = reverse('klubevents:detail', args=(past_event.id,))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Past Test')


class AttendingSubmitTests(TestCase):
    def test_attending_submit_successful(self):
        """A member should be able to mark themselves as attending an event.

        If this member does not exist, then they should be made.
        """
        # create initial event
        when = timezone.now() + datetime.timedelta(30)
        event = create_event(days=-7, name='Member Test',
                             description='Member Test', date=when,
                             location='123 Fake Street')

        # submit an attending notification
        url = reverse('klubevents:attending_submit', args=(event.id,))
        resp = self.client.post(url, {
            'name': DEFAULT_MEMBER_NAME,
            'email': DEFAULT_MEMBER_EMAIL,
        })

        # update model and check attendees
        event.refresh_from_db()
        attendees = event.attendees.all()
        self.assertQuerysetEqual(
            attendees,
            ['<Member: {} <{}>>'.format(DEFAULT_MEMBER_NAME,
                                        DEFAULT_MEMBER_EMAIL)]
        )
        member = Member.objects.get(pk=attendees[0].id)
        self.assertEqual(member.name, DEFAULT_MEMBER_NAME)
        self.assertEqual(member.email, DEFAULT_MEMBER_EMAIL)

        # make sure redirect works
        expected = reverse('klubevents:attending_success',
                           args=(event.id, attendees[0].id))
        self.assertEqual(resp.url, expected)

        # check redirect content
        resp = self.client.get(resp.url)

        expected = 'Thanks for attending Member Test, {}'.format(
            DEFAULT_MEMBER_NAME
        )
        self.assertContains(resp, expected)

    def test_attending_submit_successful_existing_member(self):
        """If a member already exists with the same email, marking them as
        attending should not make a new member.
        """
        when = timezone.now() + datetime.timedelta(30)
        event = create_event(days=-7, name='Member Test',
                             description='Member Test', date=when,
                             location='123 Fake Street')
        member = create_member()

        # submit an attending notification
        url = reverse('klubevents:attending_submit', args=(event.id,))
        resp = self.client.post(url, {
            # name shouldn't matter
            'name': 'JUNK',
            'email': DEFAULT_MEMBER_EMAIL,
        })

        event.refresh_from_db()
        attendees = event.attendees.all()

        self.assertEqual(attendees[0].id, member.id)

    def test_attending_submit_successful_non_exiting_member(self):
        """If a member does not already exist in the system, they should be
        added.
        """
        when = timezone.now() + datetime.timedelta(30)
        event = create_event(days=-7, name='Member Test',
                             description='Member Test', date=when,
                             location='123 Fake Street')
        member = create_member()

        # submit an attending notification
        url = reverse('klubevents:attending_submit', args=(event.id,))
        resp = self.client.post(url, {
            'name': 'Test User',
            'email': 'test.user@example.com',
        })

        event.refresh_from_db()
        attendees = event.attendees.all()

        self.assertGreater(attendees[0].id, member.id)

    def test_attending_submit_missing_name(self):
        """If a user tries to submit as attending without a name, we should
        error.
        """
        when = timezone.now() + datetime.timedelta(30)
        event = create_event(days=-7, name='Member Test',
                             description='Member Test', date=when,
                             location='123 Fake Street')

        url = reverse('klubevents:attending_submit', args=(event.id,))
        resp = self.client.post(url, {
            'name': 'Test User',
        })

        event.refresh_from_db()
        self.assertFalse(event.attendees.all())

        # the form should refill itself, so this should be on the page
        self.assertContains(resp, 'Test User')

    def test_attending_submit_missing_name(self):
        """If a user tries to submit as attending without an email, we should
        error.
        """
        when = timezone.now() + datetime.timedelta(30)
        event = create_event(days=-7, name='Member Test',
                             description='Member Test', date=when,
                             location='123 Fake Street')

        url = reverse('klubevents:attending_submit', args=(event.id,))
        resp = self.client.post(url, {
            'email': 'testuser@example.com',
        })

        event.refresh_from_db()
        self.assertFalse(event.attendees.all())

        # the form should refill itself, so this should be on the page
        self.assertContains(resp, 'testuser@example.com')


class MemberRegistrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MemberRegistrationTests, cls).setUpClass()
        cls.url = reverse('klubevents:member_registration')

    def test_render_registration_form(self):
        """Ensure the registration form renders."""
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Sign Up and Drink With Us!", resp.content)

        labels = [
            b'Email',
            b'Your name',
            b'Password',
            b'Confirm password',
        ]

        for label in labels:
            self.assertIn(label, resp.content)

        inputs = [
            b'name="email"',
            b'name="full_name"',
            b'name="password"',
            b'name="confirm_password"',
        ]

        for input_ in inputs:
            self.assertIn(input_, resp.content)
