# Create your views here.
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)

from rest_framework import status
from rest_framework import generics
# from rest_framework.templatetags.rest_framework import items
from rest_framework.views import APIView
from rest_framework.response import Response
# from yaml import serialize


from .models import ewsitem
# from .models import ewsitem, log, pwp_exch_model
from .forms import ewsitemForm

from .serializers import ewsitemSerializer
import logging

log = logging.getLogger(__name__)
# from todo_manager.common import conf_logging


def about(request):
    return render(
        request,
        template_name="about.html",
    )


# Здесь определяем Functional Based View
def index_view(request: HttpRequest) -> HttpResponse:  # Описываем действия
    # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
    # conf_logging(level=logging.DEBUG)
    ews_items = ewsitem.objects.all()[:3]  # свойство objects есть в БД сортировкой по id. Выводим 3 элемента
    # ews_items = ewsitem.objects.get(pk=pk)  # действия для Functional view -> если не нашли - делаем, исключение
    # ews_items = ewsitem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id

    return render(
        request,
        template_name="ews_list/index.html",
        context={"ews_items": ews_items},  # Обращение в БД за всеми элементами
        # context={"ews_items": ews_items[:3]}  # Обращение в БД за всеми элементами c показом 3-х
    )

# Процедура по обработки запроса, но вне поля видимости основного приложения ews_list
# [15/Sep/2024 20:16:15] "GET /ews/postewsitem/ HTTP/1.1" 200 15222  --> это при минимуме объявления
# [2024-09-15 20:22:21.325]        log:248 WARNING - Not Found: /ewsitem/
# [15/Sep/2024 20:22:21] "POST /ewsitem/ HTTP/1.1" 404 16665 --> при развернутом объявлении
# def postewsitem(request):
def postewsitem(request: HttpRequest) -> HttpResponse:
    # получаем из данных запроса POST отправленные через форму данные
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ewsitemForm(request.POST)
        serializer = ewsitemSerializer(data=form.cleaned_data)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # return HttpResponseRedirect("/thanks/")
            return Response(request, "ews_list/ewsitem_add.html", {"ewsform": form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ewsitemForm()

    return render(request, "ews_list/ewsitem_add.html", {"ewsform": form})

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


# # Класс для отображения содержимого БД или внесения изменений в БД. Основано на rest_framework
# class ewsitemAPIView(APIView):
#
#     def get(self, request):
#         item = ewsitem.objects.all()
#         return Response({'posts': ewsitemSerializer(item, many=True).data})
#
#     def post(self, request):
#         # create a form instance and populate it with data from the request:
#         form = ewsitemForm(request.POST)
#         serializer = ewsitemSerializer(data=form.data)
#         if form.is_valid():
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         return Response(request, "ews_list/ewsitem_add.html", {"ewsform": form})
#         # return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = ewsitem.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = ewsitemSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})

