from django.urls import path
from django.views.decorators.cache import cache_page
from mailing.apps import MailingConfig
from django.conf import settings
from django.conf.urls.static import static
from mailing.views import *


app_name = MailingConfig.name


urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', cache_page(60)(HomeView.as_view()), name='home'),

    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('mail_create/', MailingCreateView.as_view(), name='mail_create'),
    path('mails/', MailingListView.as_view(), name='mails'),
    path('mail_update/<int:pk>/', MailingUpdateView.as_view(), name='mail_update'),
    path('mail_detail/<int:pk>/', MailingDetailView.as_view(), name='mail_detail'),
    path('mail_delete/<int:pk>/', MailingDeleteView.as_view(), name='mail_delete'),
    path('switch_active/<int:pk>/', switch_active, name='switch_active'),

    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/', MessagesListView.as_view(), name='messages'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('logs/', MailingLogsListView.as_view(), name='logs'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
