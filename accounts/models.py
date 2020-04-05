from django.db.models import *
from django.contrib.auth.models import User
from django.db import models
# # Create your models here.


CATEGORIES = [
    ('R', 'RESTAURANTS'),
    ('T', 'TRAVEL'),
    ('BN', 'BARS/NIGHTLIFE'),
    ('MS', 'MOVIES & SHOWS'),
    ('PK', 'PARKS'),
    ('M','MUSEUMS'),
    ('B','BOOK CLUB'),
    ('Z', 'ZOOM'),
]


class Type(Model):

    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Profile(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    city = CharField(max_length=100)
    country = CharField(max_length=100)
    your_interests = ManyToManyField(Type, null=True)
    user = OneToOneField(User, null=True, on_delete=CASCADE)
    profile_image = ImageField(upload_to='accounts/pictures', null=True, blank=True, default='static/accounts/pictures/3.jpg')
    friends = ManyToManyField('self')
    email = EmailField(unique=True)
    
    def __str__(self):
        return f'{self.email}'


class Event(Model):
    CHOICES = [
        ('VO','VOTING OPEN'),
        ('VC','VOTES CLOSED'),
        ('C','CANCELED'),

    ]
    title = models.CharField(max_length=50)   
    description= models.TextField(default='')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_events')
    invitees = models.ManyToManyField(Profile, related_name='my_events', through='EventInvitee')
    status = models.CharField(max_length=15,choices=CHOICES,default='VO')
    category = models.CharField(max_length=20,choices=CATEGORIES, default='R')


class EventInvitee(Model):
    CHOICES = [
        ('I', "I'M IN!"),
        ('O', "COUNT ME OUT:("),
        ('P', 'PENDING')

    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,choices=CHOICES,default='P')



class Date(Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='date_options')
    date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.date}'


class Location(Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.location}'


class Vote(Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    

