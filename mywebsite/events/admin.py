from django.contrib import admin

from .models import Venue
from .models import MyClubUser
from .models import Events

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Events)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display= ('name','address','phone')
    ordering = ('name',)
    search_fields = ('name','address')

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'date', 'description', 'manager', 'approved')
    list_display = ('name', 'date', 'venue')
    list_filter = ('date', 'venue')
    ordering = ('date',)