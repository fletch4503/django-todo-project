from django.db import models
import mysql.connector  # Импортируем модуль для подключения к БД MySQL
from mysql.connector import Error


# Сюда будем добавлять класс для работы с основной базой данных - class pwp_db_model(db_const): из основного кода
class pwpitem(models.Model):
    # class Meta:
    #     project_id = ("id", )  # со знаком '-' - обратная сортировка
    #     project_req_date = "Project Date"

    project_title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.project_title
