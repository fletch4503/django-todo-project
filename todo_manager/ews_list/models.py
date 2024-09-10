from django.db import models
# from exchangelib import (
#     Account,
#     Credentials,
#     Build,
#     Configuration,
#     FaultTolerance,
#     Version,
#     Message,
#     Mailbox,
#     Folder,
#     HTMLBody,
#     FileAttachment,
#     ItemAttachment,
#     EWSDateTime,
#     EWSTimeZone,
#     EWSDate,
# )


# Сюда будем добавлять класс для работы с почтой - class pwp_exch_model: из основного кода
class ewsitem(models.Model):
    class Meta:
        ordering = ("id", )  # со знаком '-' - обратная сортировка
        verbose_name = "EWS Item"
    # class Meta:
    #     project_id = ("id", )  # со знаком '-' - обратная сортировка
    #     project_req_date = "Project Date"

    email_title = models.CharField(max_length=250)   # Сюда вставляем заголовки писем с типом из exchangelib
    sender = models.CharField(max_length=250)   # адрес отправителя
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.email_title
