from datetime import timedelta
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from mailing.models import Mailing, MailingLogs


def form_mail():
    """Формирование рассылок по перодичности"""
    mails = Mailing.objects.exclude(status='finish')

    today = timezone.now()

    for mail in mails:
        if mail.stop_time is None or mail.stop_time > today.date():
            if mail.start_time.date() <= today.date():
                if mail.status == 'create':
                    mail.status = 'start'
                    mail.save()

                last_log = MailingLogs.objects.filter(mailing=mail).last()

                # Проверка расписания рассылки с учетом последнего лога рассылки
                if last_log is None or last_log.status == 'failure' or (

                        mail.frequency == 'day' and today.date() - last_log.last_try.date() >= timedelta(days=1) or (
                        mail.frequency == 'week' and today.date() - last_log.last_try.date() >= timedelta(days=7) or (
                        mail.frequency == 'month' and today.date() - last_log.last_try.date() >= timedelta(days=30)))):

                    clients = mail.mail_to.all()
                    send_mails(clients, mail)

        else:
            mail.status = 'finish'
            mail.save()


def send_mails(clients, message):
    """Отправка сообщений на почту"""
    for client in clients:
        send_mail(
            subject=message.message.theme,
            message=message.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False,
        )
        log = MailingLogs(status='success', client=client, mailing=message)
        log.save()
