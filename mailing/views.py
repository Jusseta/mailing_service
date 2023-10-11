from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView

from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Mailing, Client, MailingLogs, Message
from mailing.services import get_mailing_cache


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


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание профиля клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Добавление клиента'}
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        """Добавление владельца клиента"""
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user
            client.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Страница со списком клиентов"""
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        """Проверка на модератора и суперюзера"""
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset.all()
        else:
            queryset = queryset.filter(owner=self.request.user.id)

        return queryset


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение клиента"""
    model = Client
    fields = ('full_name', 'email', 'message',)
    extra_context = {'title': 'Изменение клиента'}
    success_url = reverse_lazy('mailing:clients')

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента"""
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('mailing:clients')

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки"""
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailing:mails')

    def form_valid(self, form):
        """Добавление владельца рассылки"""
        if form.is_valid():
            mailing = form.save()
            mailing.owner = self.request.user
            mailing.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        """Вывод списка рассылок созданного только этим пользователем"""
        kwargs = super().get_form_kwargs()
        kwargs['uid'] = self.request.user
        return kwargs


class MailingListView(LoginRequiredMixin, ListView):
    """Страница со списком рассылок"""
    model = Mailing
    extra_context = {'title': 'Рассылки'}

    def get_queryset(self):
        """Проверка на модератора и суперюзера"""
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset.all()
        else:
            queryset = queryset.filter(owner=self.request.user.id)

        return queryset


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение рассылки"""
    model = Mailing
    fields = ('message', 'mail_to', 'frequency', 'status',)
    extra_context = {'title': 'Изменение рассылки'}

    def get_success_url(self):
        return reverse_lazy('mailing:mail_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        """Вывод списка рассылок созданного только этим пользователем"""
        kwargs = super().get_form_kwargs()
        kwargs['uid'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Страница с деталями рассылки"""
    model = Mailing
    extra_context = {'title': 'Подробности рассылки'}


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки"""
    model = Mailing
    extra_context = {'title': 'Удаление рассылки'}
    success_url = reverse_lazy('mailing:mails')

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения для рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')
    extra_context = {'title': 'Создание сообщения'}

    def form_valid(self, form):
        """Добавление владельца сообщения"""
        if form.is_valid():
            mailing = form.save()
            mailing.owner = self.request.user
            mailing.save()

        return super().form_valid(form)


class MessagesListView(LoginRequiredMixin, ListView):
    """Список сообщений"""
    model = Message
    extra_context = {'title': 'Сообщения'}

    def get_queryset(self):
        """Проверка на модератора и суперюзера"""
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset.all()
        else:
            queryset = queryset.filter(owner=self.request.user.id)

        return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщений"""
    model = Message
    success_url = reverse_lazy('mailing:messages')
    extra_context = {'title': 'Удалить сообщение'}

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение сообщений"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')
    extra_context = {'title': 'Изменить сообщение'}

    def get_object(self, queryset=None):
        """Проверка на модератора и суперюзера"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_stuff:
            raise Http404('Ограничение прав доступа')
        return self.object


class MailingLogsListView(LoginRequiredMixin, ListView):
    """Страница со списком рассылок"""
    model = MailingLogs
    extra_context = {'title': 'Логи рассылки'}
