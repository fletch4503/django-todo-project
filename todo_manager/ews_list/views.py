# Create your views here.
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)

from .models import ewsitem

# Здесь определяем Functional Based View
# def index_view(request: HttpRequest) -> HttpResponse:  # Описываем действия
#     # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
#     todo_items = ToDoItem.objects.all()[:3]  # свойство objects есть в БД сортировкой по id. Выводим 3 элемента
#     # todo_items = ToDoItem.objects.get(pk=pk)  # действия для Functional view -> если не нашли - делаем, исключение
#     # todo_items = ToDoItem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id
#     return render(
#         request,
#         template_name="todo_list/index.html",
#         context={"todo_items": todo_items}  # Обращение в БД за всеми элементами
#         # context={"todo_items": todo_items[:3]}  # Обращение в БД за всеми элементами
#     )
#
#
# class ToDoListIndexView(ListView):  # делаем свой класс на основе TemplateView. Описываем действия
#     template_name = "todo_list/index.html"
#     queryset = ToDoItem.objects.all()[:3]
#     # queryset = ToDoItem.objects.order_by("-id").all()[:2]  # с сортировкой элементов
#     # model = ToDoItem
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)  # Не переопределяем класс, а добавляем в него нужные данные
#     #     context["todo_items"] = ToDoItem.objects.all()
#     #     # context["todo_item_count"] = ToDoItem.objects.all()
#     #     return context
#
#
# class ToDoListView(ListView):  # Декларируем свойства
#     # template_name = "todo_list/index.html"  # рендерим данные в этот шаблон
#     model = ToDoItem
#
#     # context_object_name = "todo_items"  # имя из todo_list\index.html в цикле
#     # def get_context_data(self, **kwargs):
#     #     print(ToDoItem._meta.app_label)  # имя приложения
#     #     print(ToDoItem._meta.model_name)  # имя модели
#     #     return super().get_context_data(**kwargs)
#
#
# class ToDoListDoneView(ListView):  # делаем свой класс на основе TemplateView. Описываем действия
#     queryset = ToDoItem.objects.filter(done=True).all()
#
#
# class ToDoDetailView(DetailView):  # делаем свой класс на основе TemplateView. Описываем действия
#     model = ToDoItem
#     # context_object_name =
#