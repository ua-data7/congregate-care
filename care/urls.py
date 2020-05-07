from django.contrib import admin
from django.urls import path
from care.sms.api import QualtricsFormUpdateWebhookAPIView
from care.sms.api import TwilioConversationCallbackAPIView
from care.sms.api import TwilioConversationListAPIView
from django.conf.urls.static import static
from django.conf import settings

from care.frontend import views as front_views

urlpatterns = [
    path('', front_views.index),
    path('admin/', admin.site.urls)
    path('api/qualtrics/webhook', QualtricsFormUpdateWebhookAPIView.as_view()),
    path('api/twilio/conversations', TwilioConversationCallbackAPIView.as_view()),
    path('api/conversations', TwilioConversationListAPIView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
