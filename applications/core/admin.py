from django.contrib import admin, messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *


class EmployerCompanyAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','name','iin','description','icon',]
    search_fields = ['user','first_name','last_name','name','iin','description','icon',]

    ordering = ('id',)
    class Meta:
        model = EmployerCompany

admin.site.register(City)
admin.site.register(Branch)

admin.site.register(EmployerCompany, EmployerCompanyAdmin)
