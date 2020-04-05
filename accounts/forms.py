from django import forms
from django.forms import ModelForm
from .models import Profile, Event, Date, Location, Vote
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.contrib.admin import widgets
from dal import autocomplete
from django.forms import DateTimeInput
from tempus_dominus.widgets import DateTimePicker
from .widgets import XDSoftDateTimePickerInput


class LoginForm(forms.Form):
    email = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'friends', 'your_interests']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['profile', 'invitees', 'status']



class DateForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%m/%d/%Y %H:%M %p']
    )
    class Meta:
        model = Date
        fields = ['date']



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location']



class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'
        exclude = ['event', 'profile']
