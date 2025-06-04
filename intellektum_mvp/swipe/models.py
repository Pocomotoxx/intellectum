from django.db import models
from django.contrib.auth.models import User

class CulturalItem(models.Model):
    ITEM_TYPES = [
        ('BOOK', 'Book'),
        ('MOVIE', 'Movie'),
        ('PAINTING', 'Painting'),
        ('MUSICIAN', 'Musician'),
        ('OTHER', 'Other'), # Generic category
    ]

    title = models.CharField(max_length=255)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    image_url = models.URLField(max_length=500, help_text="URL to the image of the item (cover, poster, etc.)")
    description = models.TextField(blank=True, help_text="Optional: Short description or relevant metadata.")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for categorization/recommendation.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_item_type_display()})"

class UserSwipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes')
    item = models.ForeignKey(CulturalItem, on_delete=models.CASCADE, related_name='user_swipes')
    liked = models.BooleanField(help_text="True for like (right swipe), False for dislike (left swipe)")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item') # User can only swipe once per item
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} swipe on {self.item.title}: {'Like' if self.liked else 'Dislike'}"
