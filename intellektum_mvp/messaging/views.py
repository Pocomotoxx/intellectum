from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm
from profiles.models import Profile # To display profile pictures

@login_required
def conversation_list_view(request):
    conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).prefetch_related('user1__profile', 'user2__profile', 'messages')
    # For each conversation, determine the other user
    display_conversations = []
    for conv in conversations:
        other_user = conv.user2 if conv.user1 == request.user else conv.user1
        last_message = conv.messages.order_by('-timestamp').first()
        display_conversations.append({
            'conversation_obj': conv,
            'other_user': other_user,
            'last_message_content': last_message.content if last_message else "No messages yet.",
            'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count() # Basic unread count
        })
    return render(request, 'messaging/conversation_list.html', {'conversations': display_conversations})

@login_required
def conversation_detail_view(request, conversation_id):
    # Corrected query to ensure user is part of the conversation
    conversation = get_object_or_404(Conversation, Q(id=conversation_id) & (Q(user1=request.user) | Q(user2=request.user)))

    # Ensure the logged-in user is part of this conversation (already handled by Q object, but explicit check is fine for clarity)
    if request.user != conversation.user1 and request.user != conversation.user2:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You are not part of this conversation.")

    other_user = conversation.user2 if conversation.user1 == request.user else conversation.user1

    # Mark messages as read (simple implementation)
    messages_to_mark_read = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    messages_to_mark_read.update(is_read=True)

    if request.method == 'POST':
        if 'send_message' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = request.user
                message.conversation = conversation
                message.save() # Signal will handle count updates and reveal status
                return redirect('conversation_detail', conversation_id=conversation.id)
        elif 'request_reveal' in request.POST and conversation.can_request_early_reveal:
            if request.user == conversation.user1:
                conversation.user1_requests_reveal_at_10 = True
            elif request.user == conversation.user2:
                conversation.user2_requests_reveal_at_10 = True
            # The save needs to include all fields that might be changed by update_image_reveal_status too
            # or rely on update_image_reveal_status to save itself.
            # Let's ensure fields are explicitly mentioned if not relying on the model's save method fully.
            update_fields = []
            if request.user == conversation.user1:
                update_fields.append('user1_requests_reveal_at_10')
            else:
                update_fields.append('user2_requests_reveal_at_10')

            conversation.save(update_fields=update_fields)
            conversation.update_image_reveal_status() # This method saves if status changes
            return redirect('conversation_detail', conversation_id=conversation.id)

    message_form = MessageForm()
    messages = conversation.messages.all().order_by('timestamp')

    # Profile picture visibility logic
    other_user_profile = Profile.objects.get(user=other_user) # Assuming profile always exists
    show_other_user_pic = conversation.images_are_revealed

    context = {
        'conversation': conversation,
        'other_user': other_user,
        'other_user_profile': other_user_profile,
        'show_other_user_pic': show_other_user_pic,
        'messages': messages,
        'message_form': message_form,
        'can_request_reveal': conversation.can_request_early_reveal and \
                              not conversation.images_are_revealed and \
                              not (request.user == conversation.user1 and conversation.user1_requests_reveal_at_10) and \
                              not (request.user == conversation.user2 and conversation.user2_requests_reveal_at_10)
    }
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def start_conversation_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('profile_view')

    conversation, created = Conversation.get_or_create_conversation(request.user, other_user)
    return redirect('conversation_detail', conversation_id=conversation.id)
