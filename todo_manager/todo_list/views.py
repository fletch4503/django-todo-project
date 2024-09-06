from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render

from .models import ToDoItem


# Create your views here.
def index_view(request: HttpRequest) -> HttpResponse:
    todo_items = ToDoItem.objects.all()  # свойство objects есть в БД сортировкой по id
    # todo_items = ToDoItem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id
    return render(
        request,
        template_name="todo_list/index.html",
        context={"todo_items": todo_items}
    )
