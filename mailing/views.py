from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView

from mailing.forms import ClientForm, MailingForm
from mailing.models import Mailing, Client, MailingLogs
from mailing.services import get_mailing_cache
from users.models import User


def contacts(request):
    """Страница контактов"""
    return render(request, 'mailing/contacts.html')


class HomeView(LoginRequiredMixin, TemplateView):
    """Домашняя страница"""
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = get_mailing_cache()
        return context_data


class ClientCreateView(CreateView):
    """Создание профиля клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Добавление клиента'}
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user
            client.save()

        return super().form_valid(form)


class ClientListView(ListView):
    """Страница со списком клиентов"""
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user.id)

        return queryset


class ClientUpdateView(UpdateView):
    """Изменение клиента"""
    model = Client
    fields = ('full_name', 'email', 'message',)
    extra_context = {'title': 'Изменение клиента'}
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('mailing:clients')


class MailingCreateView(CreateView):
    """Создание рассылки"""
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailing:mails')


class MailingListView(ListView):
    """Страница со списком рассылок"""
    model = Mailing
    extra_context = {'title': 'Рассылки'}


class MailingUpdateView(UpdateView):
    """Изменение рассылки"""
    model = Mailing
    fields = ('message', 'mail_to', 'frequency', 'status',)
    extra_context = {'title': 'Изменение рассылки'}
    success_url = reverse_lazy('mailing:mails')


class MailingDetailView(DetailView):
    """Страница с деталями рассылки"""
    model = Mailing
    extra_context = {'title': 'Подробности рассылки'}


class MailingDeleteView(DeleteView):
    """Удаление рассылки"""
    model = Mailing
    extra_context = {'title': 'Удаление рассылки'}
    success_url = reverse_lazy('mailing:mails')


class MailingLogsListView(ListView):
    """Страница со списком рассылок"""
    model = MailingLogs
    extra_context = {'title': 'Логи рассылки'}
