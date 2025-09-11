from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from messaging.models import Message
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        logout(request)  # log the user out first
        user.delete()    # triggers post_delete signal
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")  # redirect to home page or landing page
    return render(request, "messaging/delete_user.html")

def get_threaded_replies(message):
    """
    Recursively fetch all replies to a message
    and return them in a nested structure.
    """
    replies = []
    for reply in message.replies.all().select_related('sender', 'receiver'):
        replies.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return replies


@login_required
def inbox(request):
    top_messages = Message.objects.filter(sender=request.user, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    threaded_data = []
    for msg in top_messages:
        threaded_data.append({
            'message': msg,
            'replies': get_threaded_replies(msg)
        })

    return render(request, 'messaging/inbox.html', {'threaded_data': threaded_data})


@login_required
def unread_inbox(request):
    unread_messages = (
        Message.unread
        .unread_for_user(request.user)
        .select_related('sender')
        .only('id', 'sender', 'content', 'timestamp', 'parent_message')
    )

    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})
