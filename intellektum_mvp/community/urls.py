from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.topic_list_view, name='topic_list'),
    path('forum/topic/create/', views.create_topic_view, name='create_topic'),
    path('forum/topic/<int:topic_id>/', views.topic_detail_view, name='topic_detail'),

    path('events/', views.event_list_view, name='event_list'),
    path('events/create/', views.create_event_view, name='create_event'), # Staff only
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
]
