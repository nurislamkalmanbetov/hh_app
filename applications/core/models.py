from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EmployerCompany(models.Model):
    first_name = models.CharField(_('Имя'), max_length=50, )
    last_name = models.CharField(_('Фамилия'), max_length=50,)
    position = models.CharField(_('Должность'), max_length=50, )
    contact_info = models.CharField(_('Контактные данные'), max_length=200,blank=True,)
    contact_person = models.CharField(_('Контактное лицо'), max_length=50,blank=True, )
    icon = models.ImageField(upload_to='company_icons/', blank=True, verbose_name=_('Изображение'))
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True, verbose_name=_('Работодатель'))
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    iin = models.CharField(_('ИИН/БИН'), max_length=50, blank=True,)
    payment_info = models.CharField(_('Реквезиты компании'), blank=True,max_length=255)
    description = models.TextField(_('Описание'), blank=True, default='')
    

    def __str__(self):
        return f"{self.name} | {self.user.email}"

    class Meta:
        indexes = [
            models.Index(fields=['user',]),
        ]

        verbose_name = _('Работодатель')
        verbose_name_plural = _('Работодатели')


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Земля')
        verbose_name_plural = _('Земли')


class Branch(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,null=True, verbose_name=_('Земля'))
    city = models.CharField(_('Название города'), max_length=255, blank=True,)
    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Компания'))
    name = models.CharField(_('Название филлиала'), max_length=255)
    address = models.CharField(_('Текстовый адрес'), max_length=255,)
    link_address = models.CharField(_('Ссылка на адрес'), max_length=255,)    
    description = models.TextField(_('Описание как добраться'), blank=True,)


    def __str__(self):
        return self.name

    class Meta:

        indexes = [
            models.Index(fields=['country',]),
            models.Index(fields=['company',]),

        ]


        verbose_name = _('Филиал')
        verbose_name_plural = _('Филиалы')


class Housing(models.Model):
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    
    housing_type = models.CharField(_('Тип жилья'), max_length=100)
    housing_cost = models.PositiveIntegerField(_('Стоимость жилья'), default=0)
    additional_expenses = models.TextField(_('Дополнительные расходы'), blank=True)
    deposit = models.PositiveIntegerField(_('Залог'), default=0)
    cleaning = models.CharField(_('Уборка'), max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def __str__(self):
        return self.employer.name

    class Meta:
        indexes = [
            models.Index(fields=['employer',]),

        ]
        verbose_name = _('Жилье')
        verbose_name_plural = _('Жилье')



class FilesHousing(models.Model):
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE, verbose_name=_('Жилье'))
    files = models.FileField(upload_to='housing_files/', blank=True, verbose_name=_('Файлы жилья'))

    def __str__(self):
        return self.files.url
    
    class Meta:
        verbose_name = _('Файл жилья')
        verbose_name_plural = _('Файлы жилья')

class Vacancy(models.Model):
    GENDER_CHOICES = (
        ('Male', _('Мужской')),
        ('Female', _('Женский')),
        ('Any', _('Неважно')),
    )

    KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    )


    employer_company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
  
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True, verbose_name=_('Филиал'))
    position = models.CharField(max_length=255, verbose_name=_('Позиция'))
    duty = models.TextField(_('Обязанности'),)
    is_excperience = models.BooleanField(_('Опыт работы требуется'), default=False)
    experience = models.TextField(_('Опыт работы'),)
    clothingform = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Форма одежды'))
    salary = models.PositiveIntegerField(_('Зарплата'), default=0)
    vehicle = models.CharField(max_length=100, null=True, blank=True,verbose_name=_('Транспорт'))
    insurance = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Страховка'))
    requirements = models.TextField(_('Требования работы'),null=True, blank=True,)
    conditions = models.TextField(_('Условия работы'),null=True, blank=True,)
    employee_count = models.PositiveIntegerField(_('Количество работников'), default=1)
    employee_count_hired = models.PositiveIntegerField(_('Количество нанятых работников'), default=0)
    gender = models.CharField(_('Пол'),choices=GENDER_CHOICES,max_length=50)
    time_start = models.TimeField(_('Время начала работы'))
    time_end = models.TimeField(_('Время окончания работы'))
    housing = models.ForeignKey(Housing, on_delete=models.SET_NULL, null=True, verbose_name=_('Жилье'))
    phone = models.CharField(_('Телефон'), max_length=50,blank=True,)
    description = models.TextField(_('Коментарий'), blank=True, default='')
    start_holidays_date = models.DateField(_('Дата начала каникул'),)
    end_holidays_date = models.DateField(_('Дата окончания каникул'),)
    housing_status = models.BooleanField(_('Жилье предоставляется'), default=False)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    language_german = models.CharField(_('Знание немецкого языка'), max_length=50,   choices=KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES, blank=True, null=True)
    language_english = models.CharField(_('Знание английского языка'), max_length=50, choices=KNOWLEGE_OF_LANGUAGES_LEVEL_CHOICES, blank=True,null=True)
    is_active = models.BooleanField(_('Активный'), default=True)
    

    def __str__(self):
        return self.employer_company.name

    class Meta:
        indexes = [
            models.Index(fields=['employer_company',]),

        ]
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')




class Invitation(models.Model):
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name=_('Вакансия'))
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
    is_rejected = models.BooleanField(_('Отклонено'), default=False)
    is_accepted = models.BooleanField(_('Принято'), default=False)
    is_work = models.BooleanField(_('Работает'), default=False)

    def __str__(self):
        return self.vacancy.employer_company.name
    

    class Meta:
        indexes = [
            models.Index(fields=['employer',]),
            models.Index(fields=['vacancy',]),
            models.Index(fields=['user',]),
        ]
        verbose_name = _('Приглашение на вакансию')
        verbose_name_plural = _('Приглашения на вакансии')


class Interviews(models.Model):
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name=_('Вакансия'))
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name = 'interviews_profile',verbose_name=_('Пользователь'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
    interviews_date = models.DateTimeField(_('Дата собеседования'),)
    is_accepted = models.BooleanField(_('Принято'), default=False)
    is_work = models.BooleanField(_('Работает'), default=False)
    is_rejected = models.BooleanField(_('Не прошел'), default=False)
    is_passed = models.BooleanField(_('Прошел'), default=False)

    def __str__(self):
        return self.vacancy.employer_company.name
    

    class Meta:
        indexes = [
            models.Index(fields=['employer',]),
            models.Index(fields=['vacancy',]),
            models.Index(fields=['user',]),
        ]
        verbose_name = _('Собеседование')
        verbose_name_plural = _('Собеседования')


class Favorite(models.Model):
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def __str__(self):
        return self.employer.name
    

    class Meta:
        indexes = [
            models.Index(fields=['employer',]),
            models.Index(fields=['user',]),
        ]
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранные')