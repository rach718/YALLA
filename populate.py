import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')
django.setup()
import requests
from accounts.models import *

type_choices = [
        ('RESTAURANTS'),
        ('BARS/NIGHTLIFE'),
        ('LIVE MUSIC'),
        ('TRAVEL'),
        ('MUSEUMS'),
        ('DAY TRIPS'),
        ('NATURE'),
        ('SHOPPING')
    ]

def add_choices():
    for choice in type_choices:
        c = Type(name=choice)
        print('add_choices')
        c.save()

add_choices()

