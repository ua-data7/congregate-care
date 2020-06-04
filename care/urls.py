from django.contrib import admin
from django.urls import path
from care.sms.api import QualtricsFormUpdateWebhookAPIView
from care.sms.api import TwilioConversationCallbackAPIView
from care.sms.api import TwilioConversationListAPIView
from care.sms.api import TwilioConversationReplyAPIView
from care.sms.api import QualtricsSubmissionList
from care.sms.api import FacilityList
from care.sms.api import GetFacilityEmails
from care.sms.api import SendEmailMessageAPIView
from care.sms.api import SendSMSMessageAPIView
from care.sms.api import LiaisonList
from django.conf.urls.static import static
from django.conf import settings

from care.frontend import views as front_views

urlpatterns = [
    path('', front_views.index),
    path('admin/', admin.site.urls),
    path('api/qualtrics/webhook/', QualtricsFormUpdateWebhookAPIView.as_view()),
    path('api/twilio/conversations', TwilioConversationCallbackAPIView.as_view()),
    path('api/conversations', TwilioConversationListAPIView.as_view()),
    path('api/conversations/reply', TwilioConversationReplyAPIView.as_view()),
    path('api/submissions', QualtricsSubmissionList.as_view()),
    path('api/facilities', FacilityList.as_view()),
    path('api/emails', GetFacilityEmails.as_view()),
    path('api/liaisons', LiaisonList.as_view()),
    path('api/sendemail', SendEmailMessageAPIView.as_view()),
    path('api/sendsms', SendSMSMessageAPIView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
