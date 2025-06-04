from django import forms
from .models import ForumTopic, ForumPost, Event

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'description']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class EventForm(forms.ModelForm): # For admin/staff to create events
    event_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), help_text="Format: YYYY-MM-DD HH:MM")
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location']
