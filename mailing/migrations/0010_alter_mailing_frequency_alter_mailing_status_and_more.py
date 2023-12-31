# Generated by Django 4.2.6 on 2023-10-15 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0009_mailing_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='frequency',
            field=models.CharField(choices=[('day', 'раз в день'), ('week', 'раз в неделю'), ('month', 'раз в месяц')], default='day', max_length=20, verbose_name='Периодичность'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('finish', 'завершена'), ('create', 'создана'), ('start', 'запущена')], default='create', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='mailinglogs',
            name='status',
            field=models.CharField(choices=[('success', 'успешно'), ('failure', 'неудачно')], default='success', max_length=20, verbose_name='Статус попытки'),
        ),
    ]
