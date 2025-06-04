from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user2')

    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    # Message counts - user1 is the one with the lower ID
    messages_sent_by_user1 = models.PositiveIntegerField(default=0)
    messages_sent_by_user2 = models.PositiveIntegerField(default=0)

    user1_requests_reveal_at_10 = models.BooleanField(default=False, help_text="User1 (lower ID) requested early reveal")
    user2_requests_reveal_at_10 = models.BooleanField(default=False, help_text="User2 (higher ID) requested early reveal")

    images_are_revealed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"

    @staticmethod
    def get_or_create_conversation(user_a, user_b):
        # Ensure user1.id < user2.id
        u1, u2 = (user_a, user_b) if user_a.id < user_b.id else (user_b, user_a)
        conversation, created = Conversation.objects.get_or_create(user1=u1, user2=u2)
        return conversation, created

    @property
    def can_request_early_reveal(self):
        # True if each user has sent at least 10 messages
        return self.messages_sent_by_user1 >= 10 and self.messages_sent_by_user2 >= 10

    def update_image_reveal_status(self):
        # Rule 1: 15 messages each way
        rule1_met = self.messages_sent_by_user1 >= 15 and self.messages_sent_by_user2 >= 15
        # Rule 2: Mutual consent after 10 messages each way
        rule2_met = self.can_request_early_reveal and self.user1_requests_reveal_at_10 and self.user2_requests_reveal_at_10

        new_status = rule1_met or rule2_met
        if self.images_are_revealed != new_status:
            self.images_are_revealed = new_status
            self.save(update_fields=['images_are_revealed'])
        return self.images_are_revealed


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # Placeholder, actual read status logic can be complex

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in conversation {self.conversation.id} at {self.timestamp}"
