from django.urls import path, re_path
# from django.views.generic import TemplateView

from . import views

app_name = "todo_list"

urlpatterns = [
    path("", views.ToDoListIndexView.as_view(), name="index"),
    re_path(r'about', views.about, name="about"),
    path("<int:pk>/", views.ToDoDetailView.as_view(), name="detail"),  # Детальный вид по элементу из списка
    path("list/", views.ToDoListView.as_view(), name="list"),  # Список всех дел
    path("done/", views.ToDoListDoneView.as_view(), name="done"),  # Сделанные дела
    # path("",views.index_view,name="index"),
]
