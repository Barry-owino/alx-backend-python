from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import Conversation

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view or interact with it.
    """

    def has_object_permission(self, request, view, obj):
        # For conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For messages (check if user is part of the conversation)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False


class IsParticipantOfConversation(BasePermission):
    """
    Only participants of a conversation can access it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

