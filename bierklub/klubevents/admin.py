from django import forms
from django.contrib import admin

from .models import Event, Member


class EventModelForm(forms.ModelForm):
    preamble = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    additional_notes = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Event
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'number', 'date', 'location']}),
        ('Invitation', {'fields': ['preamble', 'description',
                                   'additional_notes',]}),
        ('Metadata', {'fields': ['published_date', 'attendees']}),
    ]

    form = EventModelForm
    list_display = ('name', 'location', 'number', 'date', 'is_soon',)
    list_filter = ('date',)
    search_fields = ('name', 'location',)


admin.site.register(Event, EventAdmin)
admin.site.register(Member)
