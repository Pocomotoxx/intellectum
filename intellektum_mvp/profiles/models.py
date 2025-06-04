from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    short_bio = models.TextField(blank=True)

    # Artistic Preferences
    favorite_books = models.TextField(blank=True, help_text="List your favorite books, separated by commas.")
    favorite_movies = models.TextField(blank=True, help_text="List your favorite movies, separated by commas.")
    favorite_music_genres = models.TextField(blank=True, help_text="List your favorite music genres, separated by commas.")

    # Profile Picture
    # For the MVP, we'll use a simple URL field. File uploads add complexity for this stage.
    # We can change this to ImageField later.
    profile_picture_url = models.URLField(blank=True, null=True, help_text="URL to the profile picture.")
    # Alternatively, for actual uploads:
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# It's common practice to create/update User Profile automatically when a User instance is created/updated.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
