from django import forms
from mailing.models import Client, Mailing, Message
from users.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма для добавления клиента"""
    class Meta:
        model = Client
        fields = ('full_name', 'email', 'message',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания рассылки"""
    class Meta:
        model = Mailing
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('uid')
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(owner=uid)
        self.fields['mail_to'].queryset = Client.objects.filter(owner=uid)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания сообщения"""
    class Meta:
        model = Message
        fields = ('theme', 'body',)
