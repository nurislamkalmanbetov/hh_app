from django.contrib import admin
from .models import Notification, Employee


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('data', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('data',)



class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'department', 'position', 'birthday')
    search_fields = ('first_name', 'last_name', 'department', 'position')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Notification)