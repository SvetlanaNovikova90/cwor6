# Generated by Django 4.2 on 2024-06-25 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="имя")),
                ("surname", models.CharField(max_length=50, verbose_name="фамилия")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="почта"
                    ),
                ),
            ],
            options={
                "verbose_name": "клиент",
                "verbose_name_plural": "клиенты",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ClientsList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="название списка"),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        to="newsletter.client", verbose_name="клиент для списка"
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "список клиентов для рассылки",
                "verbose_name_plural": "список клиентов для рассылки",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(auto_now=True, verbose_name="дата создания"),
                ),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("*/1 * * * *", "каждую минуту"),
                            ("0 0 * * *", "раз в день"),
                            ("0 0 * * 0", "раз в неделю"),
                            ("0 0 1 * *", "раз в месяц"),
                        ],
                        max_length=50,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="создана", max_length=50, verbose_name="статус"
                    ),
                ),
                (
                    "name_mailing",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="название рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="блокировка рассылки"
                    ),
                ),
                (
                    "clients_list",
                    models.ManyToManyField(
                        to="newsletter.clientslist",
                        verbose_name="список клиентов для рассылки",
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылка",
                "ordering": ("name_mailing",),
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "theme",
                    models.CharField(
                        max_length=100, verbose_name="тема сообщения для рассылки"
                    ),
                ),
                ("text", models.TextField(verbose_name="текст сообщения для рассылки")),
                (
                    "mailing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="newsletter.mailing",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LogMailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="дата последней попытки"
                    ),
                ),
                (
                    "status",
                    models.CharField(max_length=20, verbose_name="статус попытки"),
                ),
                (
                    "server_response",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="ответ почтового сервера",
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="newsletter.mailing",
                    ),
                ),
            ],
        ),
    ]