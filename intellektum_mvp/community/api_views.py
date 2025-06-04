from django.http import JsonResponse
from django.utils import timezone
from .models import ForumTopic, Event


def topic_list(request):
    topics = ForumTopic.objects.all().order_by('-last_post_at', '-created_at')
    data = [
        {
            'id': topic.id,
            'title': topic.title,
            'description': topic.description,
            'created_by': topic.created_by.username if topic.created_by else None,
            'created_at': topic.created_at.isoformat(),
            'last_post_at': topic.last_post_at.isoformat() if topic.last_post_at else None,
        }
        for topic in topics
    ]
    return JsonResponse({'topics': data})


def upcoming_events(request):
    events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'event_date': event.event_date.isoformat(),
            'location': event.location,
            'created_by': event.created_by.username if event.created_by else None,
            'created_at': event.created_at.isoformat(),
        }
        for event in events
    ]
    return JsonResponse({'events': data})
