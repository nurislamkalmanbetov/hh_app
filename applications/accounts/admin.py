
from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import ManyToManyField, Q
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    # fields = ['email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ]
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'verification_code', 'password','role', 'is_delete',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser','user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1','password2', 'is_delete', 'is_active', 'is_superuser', ),
        }),
    )
    list_display = ['id','email','verification_code', 'phone',  'is_staff', 'is_delete', 'is_active','role', 'is_superuser', ]
    search_fields = ['email', 'phone',  ]
    list_editable = ['is_staff', 'is_delete', 'is_active','role',  'is_superuser',]
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')


    class Meta:
        model = User

        
admin.site.register(User, UserAdmin)
