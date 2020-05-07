from rest_framework import serializers
from care.sms.models import EnrolledUser, TwilioConversation, TwilioMessage


class EnrolledUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnrolledUser
        fields = (
            'identity',
        )


class TwilioMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = TwilioMessage
        fields = (
            'body',
            'index',
            'user',
            'created_date',
        )


class TwilioConversationSerializer(serializers.ModelSerializer):
    twiliomessage_set = TwilioMessageSerializer(many=True, read_only=True)

    class Meta:
        model = TwilioConversation
        fields = (
            'sid',
            'twiliomessage_set',
            'account_sid',
            'chat_service_sid',
            'messaging_service_sid',
            'created_date',
            'last_modified',
        )
