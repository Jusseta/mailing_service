from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView, ListView
from users.forms import UserRegisterForm, UserLoginForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    """Вход в учетную запись"""
    form_class = UserLoginForm
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Отпавка сообщения с токеном на почту для активации учетной записи"""
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.token = get_random_string(length=15)
            self.object.save()
            send_mail(
                subject='Верификация пользователя',
                message=f'Для завершения регистрации пройдите по ссылке http://127.0.0.1:8000/users/verify_{self.object.token}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
            return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def verify(request, key):
    """Подтверждение учетной записи пользователя"""
    user_item = get_object_or_404(User, token=key)
    user_item.is_active = True
    user_item.save(update_fields=['is_active'])
    return render(request, 'users/verify_message.html')


class ProfileListView(ListView):
    """Список пользователей сервиса"""
    model = User
    success_url = reverse_lazy('users:profiles')
    extra_context = {'title': 'Пользователи'}

    def get_queryset(self):
        """Проверка на модератора и суперюзера"""
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset.all()
        else:
            queryset = queryset.filter(owner=self.request.user.id)

        return queryset


def switch_active(request, pk):
    """Активирует и блокирует пользователей"""
    mailing = get_object_or_404(User, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True
    mailing.save()

    return redirect(reverse('users:profiles'))
