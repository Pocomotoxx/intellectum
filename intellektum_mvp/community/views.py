from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import ForumTopic, ForumPost, Event, EventParticipation
from .forms import ForumTopicForm, ForumPostForm, EventForm
from django.urls import reverse

# Forum Views
@login_required
def topic_list_view(request):
    topics = ForumTopic.objects.all().order_by('-last_post_at', '-created_at')
    return render(request, 'community/topic_list.html', {'topics': topics})

@login_required
def topic_detail_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    posts = topic.posts.all().select_related('author', 'author__profile')
    if request.method == 'POST':
        post_form = ForumPostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.topic = topic
            new_post.author = request.user
            new_post.save()
            topic.update_last_post_at(new_post.created_at)
            return redirect('topic_detail', topic_id=topic.id)
    else:
        post_form = ForumPostForm()
    return render(request, 'community/topic_detail.html', {'topic': topic, 'posts': posts, 'post_form': post_form})

@login_required
def create_topic_view(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.last_post_at = timezone.now() # Initialize last_post_at
            topic.save()
            return redirect(topic.get_absolute_url())
    else:
        form = ForumTopicForm()
    return render(request, 'community/create_topic.html', {'form': form})

# Event Views
@login_required
def event_list_view(request):
    events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    return render(request, 'community/event_list.html', {'events': events})

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participations = event.participations.all().select_related('user', 'user__profile')
    user_participation = participations.filter(user=request.user).first()

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in [s[0] for s in EventParticipation.STATUS_CHOICES]:
            EventParticipation.objects.update_or_create(
                user=request.user,
                event=event,
                defaults={'status': status}
            )
        elif 'remove_participation' in request.POST and user_participation:
            user_participation.delete()
        return redirect('event_detail', event_id=event.id)

    return render(request, 'community/event_detail.html', {
        'event': event,
        'participations': participations,
        'user_participation': user_participation,
        'status_choices': EventParticipation.STATUS_CHOICES
    })

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect(event.get_absolute_url())
    else:
        form = EventForm()
    return render(request, 'community/create_event.html', {'form': form})
