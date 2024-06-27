from django.db import models

from config.settings import TIME_CHOICES
from users.models import User, NULLABLE


class Client(models.Model):
    """
    Модель для создания клиента
    """
    name = models.CharField(max_length=50, verbose_name='имя')
    surname = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(unique=True, verbose_name='почта')

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('name',)


class ClientsList(models.Model):
    """
    Модель для создания списка клиентов для рассылки
    """

    partner = models.ForeignKey(User, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='клиент для списка')
    name = models.CharField(max_length=100, verbose_name='название списка')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'список клиентов для рассылки'
        verbose_name_plural = 'список клиентов для рассылки'
        ordering = ('name',)


class Mailing(models.Model):
    """
    Модель для настройки рассылки
    """
    partner = models.ForeignKey(User, on_delete=models.CASCADE)
    clients_list = models.ManyToManyField(ClientsList, verbose_name='список клиентов для рассылки')
    date = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата создания')
    periodicity = models.CharField(max_length=50, verbose_name='периодичность', choices=TIME_CHOICES)
    status = models.CharField(max_length=50, default='создана', verbose_name='статус')
    name_mailing = models.CharField(max_length=50, verbose_name='название рассылки', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='блокировка рассылки')

    def __str__(self):
        return f'{self.name_mailing}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылка'
        ordering = ('name_mailing',)
        permissions = [
            (
                'can_blocked',
                'can_blocked'
            )
        ]


class Message(models.Model):
    """
    Модель для сообщения
    """
    mailing = models.OneToOneField(Mailing, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, verbose_name='тема сообщения для рассылки')
    text = models.TextField(verbose_name='текст сообщения для рассылки')


class LogMailing(models.Model):
    """
    Модель для логов рассылки
    """
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    last_date = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата последней попытки')
    status = models.CharField(max_length=20, verbose_name='статус попытки')
    server_response = models.CharField(max_length=200, verbose_name='ответ почтового сервера', **NULLABLE)
