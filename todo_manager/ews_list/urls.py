from django.urls import (
    path,
    re_path,
    include,
)
# from django.views.generic import TemplateView

from . import views

app_name = "ews_list"

urlpatterns = [
    path("", views.EWSListIndexView.as_view(), name="index"),
    re_path(r'about', views.about, name="about"),
    path("<int:pk>/", views.EWSDetailView.as_view(), name="detail"),
    path("list/", views.EWSListView.as_view(), name="list"),
    path("done/", views.EWSListDoneView.as_view(), name="done"),
    # path("ewsitem/", views.ewsitemAPIView.as_view(), name="add"),
    path("postewsitem/", views.postewsitem, name="add"),
]
