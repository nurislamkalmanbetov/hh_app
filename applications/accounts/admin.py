from django.contrib import admin
from .models import (
    User, Profile, Rating, WorkExperience,
    Review, WorkSchedule
)
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _



class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    # fields = ['email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ]
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'verification_code','is_verified_email', 'password','role', 'is_delete',)}),
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



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'value_rating', 'rating_date', 'employer',)
    search_fields = ('user__email', 'value_rating', 'employer',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('employer', 'user', 'text', 'creation_date')
    search_fields = ('user__email', 'text')




@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_company', 'company', 'position', 'start_date', 'country',)
    search_fields = ('user__email', 'company', 'position', 'country',)
    list_filter = ('type_company', 'position', 'country',)


    fieldsets = (
        (None, {'fields': ('user', )}),
        ('Details', {'fields': ('company', 'type_company', 'position',)}),
        ('Worktime', {'fields': ('start_date', 'end_date',)}),
        ('Important dates', {'fields': ('responsibilities', 'country',)}),
    )


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id', 'user', 'first_name', 'last_name', 
        'nationality','language','language_level',
      

    )
    search_fields = ('user__email', 'nationality', 'gender', 'language')
    list_filter = ('gender', 'nationality', 'language', 'language_level',)
    fieldsets = (
        (None, {'fields': (

            'user', 'first_name', 'last_name', 'midlle_name',
            'profile_photo','gender','nationality','date_of_birth',
            'inn','language','language_level',
        

            )}),

        ('Contact', {'fields': ('phone', 'whatsapp_phone_number')}),
 
    )



@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    search_fields = ('user__email',)
    fields = (
        'user', 'monday', 'tuesday', 
        'wednesday', 'thursday', 'friday', 
        'saturday', 'sunday', 
        'custom', 
        'custom_start_time', 'custom_end_time',
        )