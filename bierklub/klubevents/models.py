from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=4096)
    date = models.DateTimeField()
    number = models.IntegerField('number IRT total events')
    location = models.CharField('address of brewery', max_length=128)
    attendees = models.ManyToManyField('Member',
                                       db_table='klubevents_event_members')

    def __str__(self):
        return (self.name + ' at ' + self.location + ' on '
                + self.date.strftime('%Y-%m-%d'))


class Member(models.Model):
    name = models.CharField('full name', max_length=128)
    email = models.EmailField()
    join_date = models.DateField()

    def __str__(self):
        return self.name + ' <' + self.email + '>'

