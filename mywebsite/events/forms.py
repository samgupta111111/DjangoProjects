from django import forms
from django.forms import ModelForm
from .models import Venue, Events

#Creating a Venue Form

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip', 'phone', 'email','venue_image')
        labels = {
            'name': '',
            'address': '',
            'zip': '',
            'phone': '',
            'email': '',
            'venue_image':'',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip': forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
        }

class EventFormAdmin(ModelForm):
    class Meta:
        model = Events
        fields = ('name', 'date', 'venue', 'manager', 'description', 'attendees')
        labels = {
            'name': '',
            'date': 'YYYY-MM-DD',
            'venue': 'Venue',
            'manager': 'Manager',
            'description': '',
            'attendees':'Attendees'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
        }



class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ('name', 'date', 'venue', 'description', 'attendees')
        labels = {
            'name': '',
            'date': 'YYYY-MM-DD',
            'venue': 'Venue',
            #'manager': 'Manager',
            'description': '',
            'attendees':'Attendees'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            #'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
        }