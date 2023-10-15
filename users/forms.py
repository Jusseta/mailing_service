from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма для входа в учетную запись"""

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля"""
    class Meta:
        model = User
        fields = ('email', 'password', 'avatar', 'phone', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'readonly': 'readonly'})
        self.fields['password'].widget = forms.HiddenInput()
