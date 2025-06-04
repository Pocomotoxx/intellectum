from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Conversation

@receiver(post_save, sender=Message)
def update_conversation_on_new_message(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation

        # Update message counts
        if instance.sender == conversation.user1:
            conversation.messages_sent_by_user1 += 1
        elif instance.sender == conversation.user2:
            conversation.messages_sent_by_user2 += 1

        # Update last_message_at
        conversation.last_message_at = instance.timestamp

        conversation.save(update_fields=['messages_sent_by_user1', 'messages_sent_by_user2', 'last_message_at'])

        # Update image reveal status (this method now also saves if status changes)
        conversation.update_image_reveal_status()
