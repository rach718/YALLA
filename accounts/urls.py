from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('create_profile/', create_profile, name='create_profile'),
    path('profile/', profile, name='profile'),
    path('create_event/', create_event, name='create_event'),
    path('voting_booth/<int:event_id>', voting_booth, name='voting_booth'),
    path('events_list/', events_list, name='events_list'),
    path('all_events/', all_events, name='all_events'),
    path('profile-autocomplete/', ProfileAutocomplete.as_view(create_field='email'), name='profile_autocomplete'),
    path('how_it_works/', how_it_works, name='how_it_works'),
    path('rsvp/<int:event_id>/<int:going>', rsvp, name='rsvp'),
]

