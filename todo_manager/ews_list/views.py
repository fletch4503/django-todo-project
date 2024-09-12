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

from ews_list.models import (
    ewsitem,
    # pwp_exch_model,
)

import logging
from todo_manager.common import conf_logging

log = logging.getLogger(__name__)


def about(request):
    return render(
        request,
        template_name="about.html",
    )


# Здесь определяем Functional Based View
def index_view(request: HttpRequest) -> HttpResponse:  # Описываем действия
    # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
    conf_logging(level=logging.DEBUG)
    ews_items = ewsitem.objects.all()[:3]  # свойство objects есть в БД сортировкой по id. Выводим 3 элемента
    # ews_exch_items = pwp_exch_model.msg_cnt_list
    # total_count = 0
    # for i in range(0, len(ews_exch_items.msg_cnt_list)):
    #     total_count = total_count + ews_exch_items.msg_cnt_list[i]
    # if total_count == 0:
    #     log.warning("ews_list - У вас нет входящих сообщений!!")
    # ews_items = ewsitem.objects.get(pk=pk)  # действия для Functional view -> если не нашли - делаем, исключение
    # ews_items = ewsitem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id
    # log.warning("View Module. email_title: %s, sender: %s, done: %s",
    #             str(ews_items.email_title),
    #             str(ews_items.sender),
    #             ews_items.done)

    return render(
        request,
        template_name="ews_list/index.html",
        context={"ews_items": ews_items}  # Обращение в БД за всеми элементами
        # context={"ews_items": ews_items[:3]}  # Обращение в БД за всеми элементами
    )


class EWSListIndexView(ListView):  # делаем свой класс на основе TemplateView. Описываем действия
    template_name = "ews_list/index.html"
    queryset = ewsitem.objects.all()[:3]

    # queryset = ToDoItem.objects.order_by("-id").all()[:2]  # с сортировкой элементов
    # model = ToDoItem

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)  # Не переопределяем класс, а добавляем в него нужные данные
    #     context["ews_items"] = ewsitem.objects.all()
    #     # context["ews_item_count"] = ewsitem.objects.all()
    #     return context


class EWSListView(ListView):  # Декларируем свойства
    # template_name = "ews_list/index.html"  # рендерим данные в этот шаблон
    model = ewsitem
    # context_object_name = "ews_items"  # имя из ews_list\index.html в цикле
    # def get_context_data(self, **kwargs):
    #     print(ewsitem._meta.app_label)  # имя приложения
    #     print(ewsitem._meta.model_name)  # имя модели
    #     return super().get_context_data(**kwargs)


class EWSListDoneView(ListView):  # делаем свой класс на основе TemplateView. Описываем действия
    queryset = ewsitem.objects.filter(done=True).all()


class EWSDetailView(DetailView):  # делаем свой класс на основе TemplateView. Описываем действия
    model = ewsitem
    # context_object_name =
