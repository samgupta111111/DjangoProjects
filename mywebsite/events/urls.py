from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.all_events, name='list-events'),
    path('my_events/', views.my_events, name='my-events'),
    path('dd_venue/', views.add_venue, name='add-venue'),
    path('venues/', views.list_venue, name='list-venue'),
    path('show_venue/<int:venue_id>/', views.show_venue, name='show-venue'),
    path('event/<int:event_id>/', views.show_event, name='show-event'),
    path('approve_events/', views.approve_events, name='approve-events'),
    path('approve_event/<int:event_id>/', views.approve_event, name='approve-event'),
    path('search_venues/', views.search_venues, name='search-venues'),
    path('search_events/', views.search_events, name='search-events'),
    path('update_venue/<int:venue_id>/', views.update_venue, name='update-venue'),
    path('add_event/', views.add_event, name='add-event'),
    path('update_event/<int:event_id>/', views.update_event, name='update-event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete-event'),
    path('delete_venue/<int:venue_id>/', views.delete_venue, name='delete-venue'),
    path('venue_text/', views.venue_text, name='venue-text'),
    path('generate_event_csv/', views.generate_event_csv, name='event-csv'),
    path('generate_event_pdf/', views.generate_event_pdf, name='event-pdf'),
]
