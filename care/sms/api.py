from django.conf import settings
import requests
import datetime
from rest_framework import viewsets, permissions, generics, views
from rest_framework.response import Response
from care.sms.models import QualtricsSubmission
from care.sms.models import TwilioConversation
from care.sms.models import TwilioMessage
from care.sms.models import Facility
from care.sms.models import Binding
from care.sms.models import send_sms_message
from care.sms.models import send_email_message
from care.sms.twilio import twilio_client
from care.sms.utils import FACILITY_NEW_CASE_TPL
from care.sms import serializers
from rest_framework import parsers
from django import forms
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from twilio.rest import TwilioException
import pytz
from django.core.mail import EmailMultiAlternatives
from django.core import mail


class QualtricsFormUpdateWebhookAPIView(generics.CreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = serializers.FacilitySerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        # hopefully this is enough for authentication.
        auth_enabled = getattr(settings, 'WEBHOOK_AUTH_ENABLE', None)
        if auth_enabled is not None:
            auth_token = request.data.get('auth_token', None)
            if auth_enabled and not auth_token == settings.WEBHOOK_TOKEN:
                return Response(status=status.HTTP_403_FORBIDDEN)
        az_now = pytz.timezone('America/Phoenix').localize(pytz.datetime.datetime.now())
        # uuid is embedded data in the qualtrics survey
        uuid = request.data.get('uuid', None)
        new_cases = request.data.get('new_cases', None)
        reporting_new_cases = request.data.get('reporting_new_cases', None)
        reporting_new_cases = reporting_new_cases == 'Yes'
        filename = request.data.get('filename', None)
        facility_name = request.data.get('facility', None)
        if new_cases is None or new_cases == '':
            new_cases = 0
        else:
            try:
                new_cases = int(new_cases)
            except ValueError:
                # person entered a non-integer string...
                new_cases = 0
        if uuid:
            facility = Facility.objects.filter(identity=uuid)
            if facility.exists():
                updates = {
                    'reporting_new_cases': reporting_new_cases,
                    'last_new_cases_reported': new_cases,
                }
                if filename and len(filename) > 0:
                    updates['last_upload_date'] = az_now
                if new_cases > 0:
                    # facility will always be cluster if at any point there are new cases
                    # this will not reverse if they report no new cases in a given submission
                    updates['cluster'] = True
                facility.update(**updates)
                if new_cases > 0:
                    # new cases - send email to Liaison.
                    subject = FACILITY_NEW_CASE_TPL['subject'].format(facility_name=facility[0].name)
                    message = FACILITY_NEW_CASE_TPL['message'].format(facility_name=facility[0].name)
                    to_emails = settings.LIAISON_EMAIL_MAP[facility[0].liaisons]
                    email_message = EmailMultiAlternatives(subject, message, settings.SENDGRID_FROM_EMAIL, [to_emails[0]], to_emails[1:], reply_to=[settings.SENDGRID_REPLY_TO_EMAIL])
                    with mail.get_connection() as connection:
                        connection.send_messages([email_message])
                facility = facility[0]
            else:
                facility = None
        else:
            facility = None
        qualtrics_submission = QualtricsSubmission.objects.create(
            facility=facility,
            facility_name=facility_name,
            new_cases=new_cases,
            reported_new_cases=reporting_new_cases,
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
                facility = binding.facility
            except Binding.DoesNotExist:
                # address is our own Twilio number we're replying from.
                facility = None
            TwilioMessage.objects.create(
                index=int(index),
                conversation=conversation,
                body=body,
                facility=facility,
                author_sid=participant_sid,
            )
            if 'pause' in body.lower() and binding is not None:
                binding.opt_out = True
                binding.save()
            elif 'resume' in body.lower() and binding is not None:
                binding.opt_out = False
                binding.save()
        return Response(status=status.HTTP_200_OK)


class TwilioConversationListAPIView(generics.ListAPIView):
    queryset = TwilioConversation.objects.all()
    serializer_class = serializers.TwilioConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SendSMSMessageAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        bulk = request.data.get('bulk', False)
        message = request.data.get('message', None)
        if not message:
            return Response('message is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        uuid = request.data.get('uuid')
        send_sms_message(uuid, message, bulk=bulk)
        return Response(status=status.HTTP_200_OK)


class SendEmailMessageAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        bulk = request.data.get('bulk', False)
        message = request.data.get('message', None)
        subject = request.data.get('subject', None)
        if not message:
            return Response('message is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        if not subject:
            return Response('subject is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        uuid = request.data.get('uuid')
        send_email_message(uuid, subject, message, bulk=bulk)
        return Response(status=status.HTTP_200_OK)


class TwilioConversationReplyAPIView(generics.CreateAPIView):
    queryset = TwilioConversation.objects.none()
    serializer_class = serializers.TwilioConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        conversation_sid = request.data.get('conversation_sid', None)
        message = request.data.get('message', None)
        if not conversation_sid:
            return Response('conversation_sid is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        if not message:
            return Response('message is a required parameter', status=status.HTTP_400_BAD_REQUEST)
        try:
            message = twilio_client.conversations.conversations(conversation_sid).messages.create(author='system', body=message)
            return Response(message.sid, status=status.HTTP_201_CREATED)
        except TwilioException as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomPagination(PageNumberPagination):
    page_size = 10



def filter_facilities(queryset, filters):

    if 'neverSubmitted' in filters and filters['neverSubmitted'] == 'true':
        queryset = queryset.filter(last_upload_date=None)
    elif 'minDate' in filters or 'maxDate' in filters:
        subs = QualtricsSubmission.objects
        if 'minDate' in filters:
            parsed_date = datetime.datetime.strptime(filters['minDate'], r'%m/%d/%Y')
            subs = subs.filter(created_date__gte=parsed_date)

        if 'maxDate' in filters:
            parsed_date = datetime.datetime.strptime(filters['maxDate'], r'%m/%d/%Y')
            subs = subs.filter(created_date__lt=parsed_date + datetime.timedelta(days=1))

        queryset = queryset.filter(id__in=subs.values('facility'))

    if 'newCases' in filters and filters['newCases'] == 'true':
        queryset = queryset.filter(reporting_new_cases=True)
    
    if 'category' in filters:
        if filters['category'] == 'cluster':
            queryset = queryset.filter(cluster=True)
        elif filters['category'] == 'noncluster':
            queryset = queryset.filter(cluster=False)

    if 'size' in filters and filters['size'] != 'all':
        queryset = queryset.filter(facility_size=filters['size'])

    liaisons = filters.getlist('liaisons[]')
    if len(liaisons):
        queryset = queryset.filter(liaisons__in=liaisons)
    
    tags = filters.getlist('tags[]')
    if len(tags):
        queryset = queryset.filter(tags__name__in=tags)

    return queryset


class FacilityList(generics.ListAPIView):
    serializer_class = serializers.FacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    
    def get_queryset(self):
        params = self.request.query_params
        queryset = filter_facilities(Facility.objects.all(), params)

        if 'order' in params:
            queryset = queryset.order_by(params['order'])

        return queryset


class GetFacilityEmails(generics.ListAPIView):
    serializer_class = serializers.FacilityEmailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        params = self.request.query_params
        return filter_facilities(Facility.objects.all(), params)



class LiaisonList(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        liaisons = Facility.objects.order_by('liaisons').values_list('liaisons', flat=True).distinct()
        return Response(liaisons)


class QualtricsSubmissionList(generics.ListAPIView):
    serializer_class = serializers.QualtricsSubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    
    def get_queryset(self):
        params = self.request.query_params
        queryset = QualtricsSubmission.objects.all()

        if 'minDate' in params:
            parsed_date = datetime.datetime.strptime(params['minDate'], r'%m/%d/%Y')
            queryset = queryset.filter(created_date__gte=parsed_date)

        if 'maxDate' in params:
            parsed_date = datetime.datetime.strptime(params['maxDate'], r'%m/%d/%Y')
            queryset = queryset.filter(created_date__lt=parsed_date + datetime.timedelta(days=1))

        if 'newCases' in params and params['newCases'] == 'true':
            queryset = queryset.filter(reporting_new_cases=True)
    
        if 'category' in params:
            if params['category'] == 'cluster':
                queryset = queryset.filter(facility__cluster=True)
            elif params['category'] == 'noncluster':
                queryset = queryset.filter(facility__cluster=False)

        if 'size' in params and params['size'] != 'all':
            queryset = queryset.filter(facility__facility_size=params['size'])

        liaisons = params.getlist('liaisons[]')
        if len(liaisons):
            queryset = queryset.filter(liaisons__in=liaisons)

        tags = params.getlist('tags[]')
        if len(tags):
            queryset = queryset.filter(facility__tags__name__in=tags)

        if 'order' in params:
            queryset = queryset.order_by(params['order'])

        return queryset
