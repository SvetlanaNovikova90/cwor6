from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .task import send_mailing


def start():
    try:
        periodicity = send_mailing()

        scheduler = BackgroundScheduler()
        scheduler.add_job(send_mailing, trigger=CronTrigger.from_crontab(periodicity))
        scheduler.start()

    except AttributeError as e:
        # Обработка ошибки AttributeError
        print(f"Нет рассылок для отправки")

