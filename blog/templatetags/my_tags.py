from django import template

from mailing.models import Mailing, Client

register = template.Library()


@register.filter()
def mymedia(val):
    if val:
        return f'/media/{val}'
    return '#'


@register.simple_tag
def mailings_total():
    """Количество всех рассылок"""
    return len(Mailing.objects.all())


@register.simple_tag
def active_mailings():
    """Количество активных рассылок"""
    return len(Mailing.objects.filter(status='start'))


@register.simple_tag
def unique_clients():
    """Количество уникальных клиентов для рассылок"""
    clients = []
    for client in Client.objects.all():
        if client.email not in clients:
            clients.append(client.email)
    return len(clients)
