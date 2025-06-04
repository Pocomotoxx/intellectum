from django.urls import path
from . import api_views

urlpatterns = [
    path('topics/', api_views.topic_list, name='api_topic_list'),
    path('events/', api_views.upcoming_events, name='api_event_list'),
]
