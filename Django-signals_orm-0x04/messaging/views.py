from django.shortcuts import redirect
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

messages = Message.objects.filter(parent_message__isnull=True) \
    .select_related('sender', 'receiver') \
    .prefetch_related('replies')
