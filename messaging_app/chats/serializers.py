from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ValidationError
from .models import CustomUser, Conversation, Message

# 1. User Serializer with explicit CharFields
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_photo']

# 2. Message Serializer with validation example
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'is_read']

    def validate_message_body(self, value):
        if not value.strip():
            raise ValidationError("Message body cannot be empty.")
        return value

# 3. Conversation Serializer using SerializerMethodField for messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data

