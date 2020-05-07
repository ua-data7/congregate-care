from django.conf import settings
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from care.sms.models import EnrolledUser
from care.sms.models import QualtricsSubmission
from care.sms.models import TwilioConversation
from care.sms.models import TwilioMessage
from care.sms.models import Binding
from care.sms.models import send_sms_message
from care.sms.models import send_email_message
from care.sms import serializers
from rest_framework import parsers
from django import forms
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
import pytz


class QualtricsFormUpdateWebhookAPIView(generics.CreateAPIView):
    queryset = EnrolledUser.objects.all()
    serializer_class = serializers.EnrolledUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        # hopefully this is enough for authentication.
        if not request.data['auth_token'] == settings.WEBHOOK_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        az_now = pytz.timezone('America/Phoenix').localize(pytz.datetime.datetime.now())
        # uuid is embedded data in the qualtrics survey
        uuid = request.data.get('uuid', None)
        if uuid:
            user = EnrolledUser.objects.get(identity=uuid)
            reporting_new_cases = request.data.get('reporting_new_cases', None)
            reporting_new_cases = reporting_new_cases == 'Yes'
            filename = request.data.get('filename', None)
            user.reporting_new_cases = reporting_new_cases
            new_cases = request.data.get('new_cases', None)
            if new_cases is None:
                new_cases = 0
            user.last_new_cases_reported = new_cases
            if filename and len(filename) > 0:
                user.last_upload_date = az_now
            user.save()
        else:
            user = None
        facility_name = request.data.get('facility_name', None)
        if facility_name:
            facility_name = facility_name.lower()
        facility = Facility.objects.filter(name__lower__contains=facility_name)
        if facility.exists():
            facility = facility[0]
        else:
            facility = None
        qualtrics_submission = QualtricsSubmission.objects.create(
            facility=facility,
            facility_name=facility_name,
            new_cases=new_cases,
            reporting_new_cases=reporting_new_cases,
            reported_by=user
        )
        return Response(status=status.HTTP_200_OK)


class TwilioConversationCallbackAPIView(generics.CreateAPIView):
    queryset = TwilioConversation.objects.all()
    serializer_class = serializers.TwilioConversationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        event_type = request.data.get('EventType')
        author = request.data.get('Author', None)
        index = request.data.get('Index', None)
        body = request.data.get('Body', None)
        conversation_sid = request.data.get('ConversationSid', None)
        chat_service_sid = request.data.get('ChatServiceSid', None)
        participant_sid = request.data.get('ParticipantSid', None)
        # from address
        message_binding_address = request.data.get('MessagingBinding.Address', None)
        # to address
        message_binding_proxy_address = request.data.get('MessagingBinding.ProxyAddress', None)
        message_sid = request.data.get('MessageSid', None)
        account_sid = request.data.get('AccountSid', None)
        if event_type == 'onConversationAdded':
            TwilioConversation.objects.create(
                sid=conversation_sid,
                account_sid=account_sid,
                chat_service_sid=chat_service_sid,
                messaging_service_sid=messaging_service_sid,
            )
        elif event_type == 'onMessageAdded':
            conversation = TwilioConversation.objects.get(sid=conversation_sid)
            try:
                binding = Binding.objects.get(address=author)
                user = binding.user
            except Binding.DoesNotExist:
                # address is our own Twilio number we're replying from.
                user = None
            TwilioMessage.objects.create(
                index=int(index),
                conversation=conversation,
                body=body,
                user=user,
                author_sid=participant_sid,
            )
        return Response(status=status.HTTP_200_OK)


class TwilioConversationListAPIView(generics.ListAPIView):
    queryset = TwilioConversation.objects.all()
    serializer_class = serializers.TwilioConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SendSMSMessageAPIView(generics.CreateAPIView):
    queryset = EnrolledUser.objects.none()
    serializer_class = serializers.EnrolledUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        bulk = request.data.get('bulk', False)
        message = request.data.get('message', None)
        if not message:
            return Response('message is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        uuid = request.data.get('uuid')
        send_sms_message(uuid, message, bulk=bulk)
        return Response(status=status.HTTP_200_OK)


class SendEmailMessageAPIView(generics.CreateAPIView):
    queryset = EnrolledUser.objects.none()
    serializer_class = serializers.EnrolledUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        bulk = request.data.get('bulk', False)
        message = request.data.get('message', None)
        subject = request.data.get('subject', None)
        if not message:
            return Response('message is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        if not subject:
            return Response('subject is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        uuid = request.data.get('uuid')
        send_email_message(uuid, message, bulk=bulk)
        return Response(status=status.HTTP_200_OK)
