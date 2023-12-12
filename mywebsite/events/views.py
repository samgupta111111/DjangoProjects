from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date
from .models import Events, Venue
from django.http import HttpResponseRedirect
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from django.core.paginator import Paginator

def home(request):
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year
    upcoming_events = Events.objects.filter(date__month=current_month, date__gte=current_date, date__year=current_year).order_by('date')
    # popular_events = Events.objects.filter(popular=True).order_by('-attendees')[:5]

    return render(request, 'events/home.html', {
        'upcoming_events': upcoming_events,
        # 'popular_events': popular_events,
    })


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/dd_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events\dd_venue.html', {'form': form, 'submitted': submitted})


def list_venue(request):
    # venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()
    paginator = Paginator(venue_list, 3)  # Show 10 events per page
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)
    return render(request, 'events/venues.html', {
        'venue_list': venue_list,
        'venues': venues
    })


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {
        'venue': venue, 'venue_owner': venue_owner,
    })


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        venue_owners = User.objects.filter(pk__in=venues.values_list('owner', flat=True))
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues, 'venue_owners': venue_owners})
    else:
        return render(request, 'events/search_venues.html', {})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venue')
    return render(request, 'events/update_venue.html', {
        'venue': venue,
        'form': form
    })


def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
        else:
            form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)

            if not request.user.is_superuser:
                event.manager = request.user

            event.save()

            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


@login_required
def approve_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)

    if request.method == 'POST':
        event.approved = True
        event.save()
        return redirect('list-events')

    return render(request, 'events/approve_event.html', {'event': event})


@login_required
def approve_events(request):
    events = Events.objects.filter(approved=False)
    return render(request, 'events/approve_events.html', {'events': events})


def update_event(request, event_id):
    event = Events.objects.get(pk=event_id)

    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html', {
        'event': event,
        'form': form
    })


def delete_event(request, event_id):
    event = Events.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')


def delete_venue(request, venue_id):
    if request.method == 'POST':
        venue = Venue.objects.get(pk=venue_id)
        venue.delete()
        messages.success(request, 'Venue deleted successfully!')
        return redirect('list-venue')

    return render(request, 'events/delete_confirmation.html', {'venue_id': venue_id})


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    lines = []
    for v in venues:
        lines.append(f'{v}\n')

    response.writelines(lines)
    return response


def generate_event_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="event_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Event', 'Venue', 'Date', 'Manager', 'Description', 'Attendees'])

    events = Events.objects.all()

    for event in events:
        attendees = ', '.join([str(user) for user in event.attendees.all()])
        writer.writerow([str(event), event.venue, event.date, event.manager, event.description, attendees])

    return response


def generate_event_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="event_details.pdf"'

    events = Events.objects.all()

    # Create the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    # Create a list to hold the event details as paragraphs
    event_details = []

    for event in events:
        attendees = ', '.join([str(user) for user in event.attendees.all()])
        details = f"Event: {str(event)}\n" \
                  f"Venue: {event.venue}\n" \
                  f"Date: {event.date}\n" \
                  f"Manager: {event.manager}\n" \
                  f"Description: {event.description}\n" \
                  f"Attendees: {attendees}\n"
        event_details.append(Paragraph(details, getSampleStyleSheet()['BodyText']))

    # Build the event details paragraphs
    elements.extend(event_details)

    # Build the PDF document and return the response
    doc.build(elements)
    return response



def my_events(request):
    if request.user.is_authenticated:
        user = request.user.id
        events = Events.objects.filter(attendees=user)
        return render(request, 'events/my_events.html', {'events': events})

    else:
        messages.success(request, "You aren't authorized to view this page.")
        return redirect('home')


def show_event(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'events/show_event.html', {'event': event})


def search_events(request):
    searched_events = []

    if 'search' in request.GET:
        searched = request.GET['search']
        events = Events.objects.filter(name__icontains=searched)

        if events.exists():
            searched_events = events

    return render(request, 'events/search_events.html', {'searched_events': searched_events})


def all_events(request):
    current_date = datetime.now().date()
    event_list = Events.objects.filter(approved=True).order_by('-date')

    for event in event_list:
        event.days_left = (event.date.date() - current_date).days

    paginator = Paginator(event_list, 3)  # Show 3 events per page
    page_number = request.GET.get('page')
    pagee = paginator.get_page(page_number)

    return render(request, 'events/event_list.html', {
        'event_list': event_list,
        'pagee': pagee
    })
