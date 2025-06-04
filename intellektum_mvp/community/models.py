from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Forum Models
class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forum_topics')
    created_at = models.DateTimeField(auto_now_add=True)
    last_post_at = models.DateTimeField(null=True, blank=True) # To sort topics by activity

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic_detail', args=[str(self.id)])

    def update_last_post_at(self, timestamp=None):
        if timestamp:
            self.last_post_at = timestamp
            self.save(update_fields=['last_post_at'])

class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author.username} in {self.topic.title} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# Event Models
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_events') # Likely admin/staff
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])

class EventParticipation(models.Model):
    STATUS_CHOICES = [
        ('INTERESTED', 'Interested'),
        ('ATTENDING', 'Attending'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event') # User can only have one status per event

    def __str__(self):
        return f"{self.user.username} is {self.get_status_display()} in {self.event.title}"
