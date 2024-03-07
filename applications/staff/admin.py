from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('data', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('data',)

admin.site.register(Notification)