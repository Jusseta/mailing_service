from django.contrib import admin
from mailing.models import Client, Message, Mailing, MailingLogs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'status',)
    list_filter = ('frequency',)
    search_fields = ('status',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('status', 'last_try',)
    list_filter = ('last_try',)
    search_fields = ('status', 'last_try',)
