from django.contrib import admin
from pwp_list.models import pwpitem


# Register your models here.
@admin.register(pwpitem)
class PWPItemAdmin(admin.ModelAdmin):
    list_display = "id", "project_title", "done"
    list_display_links = "id", "project_title"
