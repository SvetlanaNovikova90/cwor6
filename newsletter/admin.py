from django.contrib import admin

from newsletter.models import Client, ClientsList, Mailing, Message, LogMailing

admin.site.register(Client)

admin.site.register(ClientsList)

admin.site.register(Mailing)

admin.site.register(Message)

admin.site.register(LogMailing)
