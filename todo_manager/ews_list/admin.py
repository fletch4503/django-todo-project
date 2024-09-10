from django.contrib import admin
from ews_list.models import ewsitem


# Register your models here.
@admin.register(ewsitem)
class EWSItemAdmin(admin.ModelAdmin):
    list_display = "id", "email_title", "sender", "done"
    list_display_links = "id", "email_title", "sender"
