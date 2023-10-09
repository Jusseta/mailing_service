from django.core.management import BaseCommand

from mailing.models import Mailing
from mailing.services import send_mails


class Command(BaseCommand):
    """Отправка сообщений"""
    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.exclude(status='finish')
        for mailing in mailings:
            clients = mailing.mail_to.all()
            send_mails(clients, mailing)
