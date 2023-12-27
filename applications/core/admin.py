from applications.accounts.admin_utils.inlines import VacancyInline
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'name_de', 'address', 'phone', 'site', )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractAdmin)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'patent_id', 'patent_date', 'given_by', ]

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'ФИО'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =  [
        'id', 'name',
    ]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display =  [
        'id', 'name', 'category',
    ]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display =  [
        'id', 'name', 'category', 'subcategory', 'language', 'user', 'employer_company', 'required_positions', 'salary', 'city', 'destination_point','is_vacancy_confirmed','created_date',
    ]
    list_editable =('is_vacancy_confirmed',)
    date_hierarchy = 'created_date'

@admin.register(EmployerCompany)
class EmployerCompanyAdmin(admin.ModelAdmin):
    fields = ['icon','user','name','country','description',]

    list_display = ['id','name', 'user','country',]

    search_fields = ['name', ]

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'is_review_confirmed', 'created_date')
    list_filter = ('rating', 'is_review_confirmed', 'created_date')
    search_fields = ('company__name', 'user__email', 'comment')  # предполагается, что у `EmployerCompany` есть поле `name` и у `User` есть поле `email`
    list_editable = ('is_review_confirmed',)
    readonly_fields = ('created_date', 'user', 'company', 'rating', 'comment') # чтобы некоторые поля были только для чтения
    date_hierarchy = 'created_date'
    ordering = ('-created_date', 'company')



@admin.register(ProfileCounter)
class ProfileCounterAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'amount_of_profiles', ]


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    fields = (('amount_in_digits', 'amount_in_text'), )

    list_display = ['amount_in_digits', ]

@admin.register(ReviewVacancy)
class ReviewVacancyAdmin(admin.ModelAdmin):
    list_display = ['status', 'applicant_profile', 'employer', 'vacancy', 'employer_comment']
    search_fields = ['status']

    def save_model(self, request, obj, form, change):
        if not obj.employer.is_active:
            messages.add_message(request, messages.ERROR, 'Работодатель не активен и не может отправлять сообщения.')
            return  # Если работодатель не активен, модель не будет сохранена

        if not obj.employer.is_employer:
            messages.add_message(request, messages.ERROR, 'Только работодатели могут отправлять сообщения.')
            return  # Если пользователь не является работодателем, модель не будет сохранена

        super().save_model(request, obj, form, change)



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('text', )
    list_editable = ('status',)
    actions = ['mark_as_DECLINED', 'mark_as_modereted']

    def mark_as_DECLINED(self, request, queryset):
        queryset.update(status='DECLINED')
    mark_as_DECLINED.short_description = 'Пометить как в Отклонен'
    def mark_as_modereted(self, request, queryset):
        queryset.update(status='MODERETED')
    mark_as_modereted.short_description = 'Пометить как в прошли модерацию'

@admin.register(ImprovementIdea)
class ImprovementIdeaAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('text',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке
    list_display = ('id', 'user', 'vacancy', 'employer', 'status', 'short_message')
    
    # Фильтры для быстрого поиска
    list_filter = ('status', 'employer')
    
    # Поиск по определенным полям
    search_fields = ('user__email', 'vacancy__name', 'employer__name')
    
    # Сортировка по умолчанию
    ordering = ('-id',)
    
    # Поля для редактирования прямо в списке
    list_editable = ('status',)

    # Разделение на поля для лучшей навигации при редактировании
    fieldsets = (
        ('General Info', {
            'fields': ('user', 'vacancy', 'employer', 'status')
        }),
        ('Message', {
            'fields': ('message',)
        }),
    )

    # Метод для отображения короткой версии сообщения в списке (первые 50 символов)
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'



def func():


    # Create a list of companies and vacancies with more detailed information
    companies = [
        {"name": "MacDonald's", "country": "USA", "description": "Fast food restaurant chain"},
        {"name": "Hotel", "country": "France", "description": "Luxury hotel with international presence"},
        {"name": "Burger King", "country": "USA", "description": "Global chain of hamburger fast food restaurants"}
    ]

    vacancies = [
        {"name": "Официант", "employer_company": 0, "salary": 10000, "city": "New York", "duty": "Serving customers"},
        {"name": "Ресепшн", "employer_company": 1, "salary": 15000, "city": "Paris", "duty": "Managing guest check-ins"},
        {"name": "Кассир", "employer_company": 2, "salary": 12000, "city": "Los Angeles", "duty": "Handling transactions"}
    ]

    # Assume you have at least one user, category, and subcategory in your database.
    default_user = User.objects.first()  # Replace with a specific user if necessary
    default_category = Category.objects.first()  # Replace with a specific category if necessary
    default_subcategory = Subcategory.objects.first()  # Replace with a specific subcategory if necessary

    # Create and save the companies with more detailed information
    created_companies = []
    for company in companies:
        new_company = EmployerCompany(
            user=default_user,
            name=company['name'],
            country=company['country'],
            description=company['description']
            # Add more fields as necessary
        )
        new_company.save()
        created_companies.append(new_company)

    # Create and save the vacancies with more detailed information
    for vacancy in vacancies:
        new_vacancy = Vacancy(
            user=default_user,
            employer_company=created_companies[vacancy['employer_company']],
            name=vacancy['name'],
            salary=vacancy['salary'],
            city=vacancy['city'],
            duty=vacancy['duty'],
            category=default_category,
            subcategory=default_subcategory,
            language="en",  # Example: replace with actual language code
            proficiency="A1",  # Example: replace with actual proficiency level
            accomodation_type="yes",  # Example: replace with actual accommodation info
            # Add more fields as necessary
        )
        new_vacancy.save()

    print("Companies and vacancies with detailed information have been added successfully.")


func()