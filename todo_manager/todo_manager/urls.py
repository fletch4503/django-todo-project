"""
URL configuration for todo_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from app import views as app_views
from django.conf import settings


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),  # Class-based views
    path("about/", TemplateView.as_view(template_name="about.html"), name="About"),
    path("todos/", include("todo_list.urls")),  # Including first URLconf
    path("ews/", include("ews_list.urls")),  # Including EWS URLconf
    # path("todos/", include("pwp_list.urls")),  # Including another URLconf
    path("admin/", admin.site.urls),
    path('sample/', app_views.sample_view),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
