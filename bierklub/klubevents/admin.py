from django.contrib import admin

from .models import Event, Member


admin.site.register([Event, Member])
