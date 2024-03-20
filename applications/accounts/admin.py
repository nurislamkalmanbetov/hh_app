from django.contrib import admin
from .models import (
    User, Profile, WorkExperience, University, PassportAndTerm, 
    Payment, Deal,
)
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'verification_code','is_verified_email', 'password', 'is_delete',)}),
        (_('Permissions'), {'fields': ('role','is_staff', 'is_active', 'is_superuser','user_permissions')}),
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
    list_editable = ['is_staff', 'is_delete', 'is_active','is_superuser',]
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')

    class Meta:
        model = User



class UniversityInline(admin.StackedInline):  
    model = University
    extra = 1


class PassportAndTermInline(admin.StackedInline):  
    model = PassportAndTerm
    extra = 1


class Payment(admin.StackedInline): 
    model = Payment
    extra = 1


class Deal(admin.StackedInline):
    model = Deal
    extra = 1

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id', 'user', 'first_name', 'last_name', 'nationality_ru',
        'german', 'english', 'russian',
    )

    search_fields = ('user', 'nationality_ru', 'gender_ru', 'english', 'russian', 'german',)
    list_filter = ('gender_ru', 'nationality_ru', 'english', 'russian', 'german',)
    fieldsets = (
        (None, {'fields': (
            'user', 'first_name', 'first_name_ru','first_name_de', 'last_name', 'last_name_ru','last_name_de',
            'middle_name', 'middle_name_ru','middle_name_de', 'profile_photo',
            'gender_ru', 'gender_en', 'gender_de',
            'nationality_ru', 'nationality_en', 'nationality_de',
            'birth_country_ru', 'birth_country_en', 'birth_country_de',
            'birth_region_ru', 'birth_region_en', 'birth_region_de',
            'date_of_birth', 'phone', 'whatsapp_phone_number',
            'german', 'english', 'russian',
        )}),
    )

    inlines = [
        UniversityInline, PassportAndTermInline, 
        Payment, Deal,]  # Добавляем в профиль инлайн университета




@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_company', 'company', 'position', 'start_date', )
    search_fields = ('user__email', 'company', 'position', 'country',)
    list_filter = ('type_company', 'position', )


    fieldsets = (
        (None, {'fields': ('user', )}),
        ('Details', {'fields': ('company', 'type_company', 'position',)}),
        ('Worktime', {'fields': ('start_date', 'end_date',)}),
        ('Important dates', {'fields': ('responsibilities', 'country',)}),
    )



