from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from community.models import Event
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Loads initial sample events into the database'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing events...')
        Event.objects.all().delete()

        # Ensure a staff user exists to be the creator, or use None
        creator = User.objects.filter(is_staff=True).first()

        events_data = [
            {'title': 'Museum Visit: Modern Art Exhibition', 'description': 'Explore the new modern art exhibit downtown.', 'event_date': timezone.now() + timedelta(days=7), 'location': 'City Art Museum', 'created_by': creator},
            {'title': 'Book Club Meetup: "The Midnight Library"', 'description': 'Discussing "The Midnight Library" by Matt Haig.', 'event_date': timezone.now() + timedelta(days=14), 'location': 'Central Library, Room A', 'created_by': creator},
            {'title': 'Indie Film Screening: "Nomadland"', 'description': 'Screening of the award-winning film Nomadland, followed by a short discussion.', 'event_date': timezone.now() + timedelta(days=21), 'location': 'Art House Cinema', 'created_by': creator},
            {'title': 'Live Jazz Night', 'description': 'An evening of live jazz music at The Blue Note cafe.', 'event_date': timezone.now() + timedelta(days=10, hours=4), 'location': 'The Blue Note Cafe', 'created_by': creator},
        ]

        self.stdout.write(f'Loading {len(events_data)} sample events...')
        for event_data in events_data:
            Event.objects.create(**event_data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample events.'))
