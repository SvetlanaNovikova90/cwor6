import pytz
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail
from mailing.models import Mailing, LogMailing


def send_mailing():
    # определение текущего времени
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    periodicity = None
    client_email = []

    # создание объекта с применением фильтра
    mailings = Mailing.objects.filter(date__lte=current_datetime).filter(
        status__in=['создана', 'запущена', 'завершена']).filter(is_active=True)

    for mailing in mailings:
        # получение временного периода
        periodicity = mailing.periodicity

        # получение списка клиентов для рассылки
        clients_lists = mailing.clients_list.all()

        # получение темы и текста сообщения для рассылки
        message = mailing.message if hasattr(mailing, 'message') else None
        text = message.text
        theme = message.theme

        log_mailing = LogMailing(mailing=mailing)

        for clients_list in clients_lists:
            # Получение клиентов из списка
            clients = clients_list.clients.all()

            for client in clients:
                # получение email клиента
                email = client.email
                client_email.append(email)

            # сбор сообщения
        try:
            send_mail(
                subject=theme,
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=client_email
            )

            mailing.status = 'запущена'
            log_mailing.status = 'успешно'

        except Exception as e:
            log_mailing.status = 'неудачно'
            log_mailing.server_response = str(e)

        finally:
            log_mailing.save()

        # обновление статуса рассылки после ее завершения
        mailing.status = 'завершена'
        mailing.save()

    return periodicity
