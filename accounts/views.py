from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout as dlogout, login as dlogin
from .models import Profile, EventInvitee
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.contrib.admin import widgets
from dal import autocomplete
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.


def home(request):
    return render(request, 'homepage.html')


def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            permission = Permission.objects.get(codename='add_profile')
            user.save()
            user.user_permissions.add(permission)
            profile,created = Profile.objects.get_or_create(email=user.email)
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            for error in form.errors:
                print(error)
    form = MyUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                dlogin(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'User or Password Not Valid, Please Try Again')
        for error in form.errors:
            messages.warning(request, error)
        return redirect('login')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})



def logout(request):
    dlogout(request)
    return redirect('home')



@login_required()
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('profile')
        messages.warning(request, 'This is not a valid form')
        return redirect('create_profile')
    else:
        form = ProfileForm()
        return render(request, 'create_profile.html', {'form':form})


def profile(request):
    return render(request,'profile.html')


def how_it_works(request):
    return render(request,'how_it_works.html')


def create_event(request):
    LocationFormSet = formset_factory(LocationForm, extra=3)
    DateFormSet = formset_factory(DateForm, extra=2)
    if request.method == 'POST':
        location_form_set = LocationFormSet(request.POST)
        date_form_set = DateFormSet(request.POST)
        form = EventForm(request.POST)
        if form.is_valid() and location_form_set.is_valid() and date_form_set.is_valid():
            event = form.save(commit=False)
            event.profile = request.user.profile
            event.save()
            invitee = EventInvitee(event=event, profile=request.user.profile)
            invitee.save()
            for email in request.POST.get('emails').splitlines():
                try:
                    validate_email(email)
                except:
                    print("bad email")
                else:
                    profile, created = Profile.objects.get_or_create(email=email)
                    # event.invitees.add(profile)
                    invitee = EventInvitee(event=event, profile=profile)
                    invitee.save()
                    request.user.profile.friends.add(profile)
            for form in location_form_set:
                location = form.save(commit=False)
                location.event = event
                location.save()
            for form in date_form_set:
                date = form.save(commit=False)
                if form.cleaned_data:
                    date.event = event
                    date.save()
            return redirect('all_events')
        for error in form.errors:
            messages.warning(request, error)
        return redirect('create_event')
    else:
        form = EventForm()
        location_form_set = LocationFormSet()
        date_form_set = DateFormSet()
        return render(request, 'create_event.html',{'form':form, 'location_forms':location_form_set, 'date_forms':date_form_set})



def all_events(request):
    votes = Vote.objects.filter(profile=request.user.profile)
    voted_events = [vote.event for vote in votes]
    events_list = request.user.profile.created_events.all() | request.user.profile.my_events.all()
    events_list = events_list.distinct()
    return render(request,'all_events.html',{'events_list':events_list,'voted_events':voted_events})


class ProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = self.request.user.profile.friends.all()
        if self.q:
            qs = qs.filter(email__istartswith=self.q)
        return qs


def voting_booth(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.profile not in event.invitees.all() and request.user.profile != event.profile:
        return redirect('all_events')
    vote = event.vote_set.filter(profile=request.user.profile).first()
    if vote:
        return redirect('all_events')
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.event = event
            vote.profile = request.user.profile
            vote.save()
            return redirect('all_events')
        return redirect('voting_booth')
    form = VoteForm()
    form.fields['date'].queryset = event.date_options.all()
    form.fields['location'].queryset = event.location_set.all()
    return render(request,'voting_booth.html',{'form':form, 'event':event})



def close_votes(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.profile == event.profile:
        event.status = 'VC'
        event.save()
    return redirect('all_events')


# def rsvp(request, event_id, going):
#     event = Event.objects.get(id=event_id)
#     print(going)
#     if request.user.profile in event.invitees.all() or request.user.profile == event.profile:
#         invitee = EventInvitee.objects.filter(event=event, profile=request.user.profile)
#         print(invitee)
#         if going == 1:
#             invitee.status = 'I'
#             invitee.save()
#         elif going == 0:
#             invitee.status = 'O'
#             invitee.save()
#     return redirect('view_event', event.id)

def rsvp(request, event_id, going):
    event = Event.objects.get(id=event_id)
    invitee = EventInvitee.objects.get(event=event, profile=request.user.profile)
    if going == 1:
        invitee.status = 'I'
    elif going == 0:
        invitee.status = 'O'
    invitee.save()
    return redirect('view_event', event.id)


def view_event(request,event_id):
    event = Event.objects.get(id=event_id)
    invitees = EventInvitee.objects.filter(event=event)
    location_vote = {}
    date_vote = {}
    winning_location_counter = 0
    winning_date_counter= 0
    for location in event.location_set.all():
        location_vote.update({location: Vote.objects.filter(event=event, location=location).count()})
    for date in event.date_options.all():
        date_vote.update({date: Vote.objects.filter(event=event, date=date).count()})
    for date,votes in date_vote.items():
        if votes >= winning_date_counter:
            winning_date = date
            winning_date_counter = votes
    for location, votes in location_vote.items():
        if votes >= winning_location_counter:
            winning_location = location
            winning_location_counter = votes
    return render(request,'view_event.html',{'event':event,'invitees':invitees,'location_vote':location_vote,
                                             'date_vote':date_vote, 'location':winning_location, 'date':winning_date})
