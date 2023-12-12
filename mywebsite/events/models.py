from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=300)
    zip = models.CharField(max_length=15)
    phone = models.CharField(max_length=25, blank=True)
    web = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    owner = models.IntegerField(blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Events(models.Model):
    name = models.CharField('Event Name', max_length=60)
    date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField(default=False)  # New field for approval

    def __str__(self):
        return self.name
