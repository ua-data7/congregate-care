from rest_framework import serializers
from care.sms.models import TwilioConversation
from care.sms.models import TwilioMessage
from care.sms.models import Facility
from care.sms.models import Binding
from care.sms.models import QualtricsSubmission


class FacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Facility
        fields = (
            'identity',
            'name',
            'facility_size',
            'cluster',
            'address',
            'liasons',
            'emails',
            'phones',
            'preferred_contact',
            'tags',
            'reporting_new_cases',
            'last_new_cases_reported',
            'last_upload_date',
            'last_modified',
            'created_date',
        )


class BindingSerializer(serializers.ModelSerializer):
    facility = FacilitySerializer(read_only=True)

    class Meta:
        model = Binding
        fields = (
            'facility',
            'binding_sid',
            'address',
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


class FacilitySerializer(serializers.ModelSerializer):
    last_upload_date = serializers.DateTimeField(format=r'%m/%d/%Y')
    last_message_date = serializers.DateTimeField(format=r'%m/%d/%Y')

    class Meta:
        model = Facility
        fields = '__all__'


class QualtricsSubmissionSerializer(serializers.ModelSerializer):
    facility = FacilitySerializer()
    created_date = serializers.DateTimeField(format=r'%m/%d/%Y')

    class Meta:
        model = QualtricsSubmission
        fields = '__all__'