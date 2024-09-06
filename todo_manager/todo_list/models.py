from django.db import models


class ToDoItem(models.Model):
    class Meta:
        ordering = ("id", )  # со знаком '-' - обратная сортировка
        verbose_name = "ToDo Item"

    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class pwpitem(models.Model):
    # class Meta:
    #     project_id = ("id", )  # со знаком '-' - обратная сортировка
    #     project_req_date = "Project Date"

    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ewsitem(models.Model):
    # class Meta:
    #     project_id = ("id", )  # со знаком '-' - обратная сортировка
    #     project_req_date = "Project Date"

    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
