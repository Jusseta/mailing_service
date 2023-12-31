# Generated by Django 4.2.6 on 2023-10-08 05:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=150, verbose_name='Почта')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала рассылки')),
                ('stop_time', models.DateTimeField(verbose_name='Дата окончания рассылки')),
                ('frequency', models.CharField(choices=[('day', 'раз в день'), ('week', 'раз в неделю'), ('month', 'раз в месяц')], default='day', verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('finish', 'завершена'), ('create', 'создана'), ('start', 'запущена')], default='create', verbose_name='Статус')),
                ('mail_to', models.ManyToManyField(to='mailing.client', verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')),
                ('status', models.CharField(choices=[('success', 'успешно'), ('failure', 'отказ')], default='success', verbose_name='Статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Сообщение'),
        ),
    ]
